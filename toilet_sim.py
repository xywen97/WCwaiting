import simpy
import numpy as np

class ToiletSimStep:
    def __init__(self, n_male, n_female, params):
        self.env = simpy.Environment()
        self.male_toilets = simpy.Resource(self.env, n_male)
        self.female_toilets = simpy.Resource(self.env, n_female)
        self.params = params
        self.n_male = n_male
        self.n_female = n_female
        self.male_wait_times = []
        self.female_wait_times = []
        self.male_queue_len = 0
        self.female_queue_len = 0
        self.male_status = [False] * n_male
        self.female_status = [False] * n_female
        self.finished = False
        self.people = 0
        self._setup()

    def _setup(self):
        self.env.process(self.arrival_process())

    def arrival_process(self):
        while True:
            gender = 'female' if np.random.rand() < self.params['female_ratio'] else 'male'
            self.env.process(self.person(gender))
            yield self.env.timeout(np.random.exponential(self.params['arrival_interval']))

    def person(self, gender):
        arrival_time = self.env.now
        if gender == 'male':
            with self.male_toilets.request() as req:
                self.male_queue_len = len(self.male_toilets.queue)
                yield req
                wait = self.env.now - arrival_time
                self.male_wait_times.append(wait)
                idx = self._find_free(self.male_status)
                if idx is not None:
                    self.male_status[idx] = True
                yield self.env.process(self.use_toilet(gender))
                if idx is not None:
                    self.male_status[idx] = False
        else:
            with self.female_toilets.request() as req:
                self.female_queue_len = len(self.female_toilets.queue)
                yield req
                wait = self.env.now - arrival_time
                self.female_wait_times.append(wait)
                idx = self._find_free(self.female_status)
                if idx is not None:
                    self.female_status[idx] = True
                yield self.env.process(self.use_toilet(gender))
                if idx is not None:
                    self.female_status[idx] = False

    def use_toilet(self, gender):
        if np.random.rand() < self.params[f'{gender}_poop_prob']:
            duration = np.random.exponential(self.params[f'{gender}_poop_time'])
        else:
            duration = np.random.exponential(self.params[f'{gender}_pee_time'])
        yield self.env.timeout(duration)

    def _find_free(self, status_list):
        for i, s in enumerate(status_list):
            if not s:
                return i
        return None

    def step(self):
        if not self.finished:
            self.env.step()
            if self.env.now >= self.params['sim_time']:
                self.finished = True

    def get_status(self):
        # 更新队列长度
        self.male_queue_len = len(self.male_toilets.queue)
        self.female_queue_len = len(self.female_toilets.queue)
        return {
            'male_status': self.male_status.copy(),
            'female_status': self.female_status.copy(),
            'male_queue_len': self.male_queue_len,
            'female_queue_len': self.female_queue_len,
            'now': self.env.now,
            'finished': self.finished
        }

def run_simulation(params):
    env = simpy.Environment()
    sim = ToiletSimStep(params['n_male'], params['n_female'], params)
    env.process(sim.arrival_process())
    env.run(until=params['sim_time'])
    return sim.male_wait_times, sim.female_wait_times 