class Param:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Metric:
    def __init__(self, key, value, timestamp, step):
        self.key = key
        self.value = value
        self.timestamp = timestamp
        self.step = step

class Tag:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Run:
    def __init__(self, name, experiment_id, start_time, end_time, status):
        self.name = name
        self.experiment_id = experiment_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.status = status
        self.params = []
        self.metrics = []
        self.tags = []
    
    def add_param(self, param):
        self.params.append(param)

    def add_metric(self, metric):
        self.metrics.append(metric)

    def add_tag(self, tag):
        self.tags.append(tag)
    
    def __str__(self):
        return f"""Run:
                    - name: {self.name}
                    - experiment_id: {self.experiment_id}
                    - start_time: {self.start_time}
                    - end_time: {self.end_time}
                    - status: {self.status}
        """



class Experiment:
    def __init__(self, name, artifact_location):
        self.name = name
        self.artifact_location = artifact_location
        self.runs = []

    def add_run(self, run):
        self.runs.append(run)

    def __str__(self):
        runs_str = '\n\t'.join([str(run) for run in self.runs])
        return f"""Experiment: 
                - name: {self.name}
                - artifact_location: {self.artifact_location}
                - runs: {runs_str}
                    """