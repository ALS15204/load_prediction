from multiprocessing import Manager, JoinableQueue, Process

from load_prediction.utils.logger import setup_logger

logger = setup_logger("multiprocessors")


class BaseMultiProcessor(object):

    def __init__(self, num_workers=2, preserve_order=True):
        self.input_queue = JoinableQueue()
        self.num_workers = num_workers
        self.processes = None
        self.m = Manager()
        self.results = self.m.list()
        self.preserve_order = preserve_order
        self._internal_data_counter = 0

    def _reset_results(self):
        del self.results[:]
        self._internal_data_counter = 0

    def _wait_for_queue_to_be_empty(self):
        """ wait until queue is empty """
        self.input_queue.join()

    def worker(self, processor, *args):
        while True:
            n, data = self.input_queue.get()
            try:
                result = processor(data, *args)
                self.results.append((n, result))
                logger.debug("task {} done".format(n if n else ""))
            finally:
                self.input_queue.task_done()

    def put_data_into_input_queue(self, input_data_list):
        for data in input_data_list:
            counter = None
            if self.preserve_order:
                counter = self._internal_data_counter
                self._internal_data_counter += 1
            self.input_queue.put((counter, data))

    def spawn_processes(self, processor, *args):
        self.processes = [Process(target=self.worker, args=(processor, *args,)) for _ in range(self.num_workers)]
        for p in self.processes:
            p.start()
            logger.debug("spawned process {}".format(p.pid))

    def terminate(self):
        for p in self.processes:
            p.terminate()
            logger.debug("terminated process {}".format(p.pid))

    def get_results(self, default_result=None):
        """
        For better data serialization
        :return:
        """
        self._wait_for_queue_to_be_empty()
        if self.preserve_order:
            results = [default_result] * len(self.results)
            for n, res in self.results:
                results[n] = res
        else:
            results = [t[1] for t in self.results]
        self._reset_results()
        return results


def pmap(processor, input_data, num_workers, default_result=None):
    multiprocessor = BaseMultiProcessor(num_workers=num_workers, preserve_order=True)
    multiprocessor.spawn_processes(processor)
    multiprocessor.put_data_into_input_queue(input_data)
    results = multiprocessor.get_results(default_result)
    multiprocessor.terminate()
    return results
