import operator
import psutil
import graphio
import humanfriendly


class StrategyBase:
    cache_storage_warning_limit = 80
    cache_storage_clogged_limit = 90
    cache_available_storage = None

    def __init__(self, manager: "neobulkmp.Manager"):
        self.manager = manager
        if self.cache_available_storage is None:
            self.cache_available_storage = (
                getattr(psutil.virtual_memory(), "total") * 0.80
            )
        else:
            self.cache_available_storage = humanfriendly.parse_size(
                self.cache_available_storage
            )

    def amount_loading_cores(self) -> int:
        if (
            self._is_sourcing_phase_done()
            or self._get_cache_size() >= self.manager.cache_size
            or self.cache_storage_level() in ["ORANGE", "RED"]
        ):
            return self.manager.cpu_count
        c = round(self.manager.cpu_count - self.amount_sourcing_cores())
        if c == 0:
            c = 1
        return c * 2

    def amount_loading_nodes_cores(self) -> int:
        c = round(self.amount_loading_cores() * 0.9)
        if c == 0:
            c = 1
        return c

    def amount_loading_rels_cores(self) -> int:
        # if we are ended the sourcing phase (all sourcing workers finished) we first load all nodesets and after that all relsets can load without draining)
        if (
            self._get_count_left_sourcing_workers() == 0
            and len(self.manager.cache.list_SetsMeta(graphio.NodeSet)) > 0
        ):
            return 0
        # if we are low on nodeSets in the cache we can start more RelSet loaders
        nodesets_cores_needed: int = len(
            self.manager.cache.list_SetsMeta(graphio.NodeSet)
            + self.manager.manager_loading._get_workers(
                status=("initial", "running"),
                tag=self.manager.manager_loading.worker_tag_nodesets,
            )
        )
        if nodesets_cores_needed < self.amount_loading_nodes_cores():
            return self.amount_loading_cores() - nodesets_cores_needed
            # else
        # By default we apply 10% of available loading cores to RelSets (or at least one Core)
        c = round(self.amount_loading_cores() * 0.1)
        if c == 0:
            c = 1
        return c

    def amount_sourcing_cores(self) -> int:
        if self.cache_storage_level() == "RED":
            return 0
        if (
            self._get_cache_size() >= self.manager.cache_size
            or self.cache_storage_level() == "ORANGE"
        ):
            #  if we maxed out the allowed cache size, slow down sourcing new data into the cache and empty the cache by mainly allow cores to load data from the cache into the DB
            c = round(self.manager.cpu_count * 0.1)
        elif self._get_count_running_sourcing_workers() >= round(
            self.manager.cpu_count * 0.6
        ):
            # provide 60% of cores if there are enough sourcing tasks
            c = round(self.manager.cpu_count * 0.6)
            # on CPUs with low core count we could round to zero cores. we want to have at least one core
            if c == 0:
                c = 1
        else:
            # if there are not many sourcing tasks left, we just provide enough cores for the leftovers
            c = self._get_count_running_sourcing_workers()
        return c

    def _get_count_running_sourcing_workers(self) -> int:
        return len(
            self.manager.manager_sourcing._get_workers(status=("initial", "running"))
        )

    def _get_count_left_sourcing_workers(self) -> int:
        return len(self.manager.manager_sourcing.workers) - len(
            self.manager.manager_sourcing._get_workers(progress="complete")
        )

    def _get_memory_consumed_by_loaders(self):
        raise NotImplementedError

    def _get_memory_consumed_by_parsers(self):
        raise NotImplementedError

    def _is_sourcing_phase_done(self):
        return self.manager.manager_sourcing.is_done()

    def _get_available_memory(self):
        return getattr(psutil.virtual_memory(), "available")

    def _get_total_memory(self):
        return getattr(psutil.virtual_memory(), "total")

    def _get_cache_size(self) -> int:
        return self.manager.cache.storage_used()

    def _get_cache_size_total(self) -> int:
        return self.cache_available_storage

    def cache_storage_level(self) -> str:
        mem_full_perc = (self._get_cache_size() * 100) / self._get_cache_size_total()
        if self.cache_storage_clogged_limit <= mem_full_perc:
            return "RED"
        elif self.cache_storage_warning_limit <= mem_full_perc:
            return "ORANGE"
        else:
            return "GREEN"

    def _get_cache_meta_data(self, sort_attr="total_size_bytes"):
        meta_data = self.manager.cache.list_SetsMeta()
        meta_data.sort(key=operator.attrgetter(sort_attr), reverse=True)
        return meta_data
