from celery import Celery, group, chain

app = Celery('tasks', broker='pyamqp://guest:guest@localhost:5672', backend='db+postgresql://postgres:password@localhost:5432/celery_logs?sslmode=disable', )

@app.task
def task_a(x):
    print("Running task_a")
    return x + 1

@app.task
def task_b(x):
    print("Running task_b")
    return x * 2

@app.task
def task_c(x):
    print("Running task_c")
    return x - 3

@app.task
def task_d(results):
    x, y = results  # Unpack the results from task_b and task_c
    print("Running task_d")
    return x + y

def create_dag(input_value):
    # Step 1: Execute task_a first
    result_a = task_a.s(input_value)
    
    # Step 2: Execute task_b and task_c concurrently
    result_b_c = group(task_b.s(), task_c.s())
    
    # Step 3: After task_b and task_c, pass their results to task_d
    final_result = chain(result_a, result_b_c, task_d.s())()
    
    return final_result