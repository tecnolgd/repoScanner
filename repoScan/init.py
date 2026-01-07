
def laodTask(file_path):
    tasks=[]

    try:
        with open(file_path,"r") as file:
            for line in file:
                task= line.strip()
                if task:
                    tasks.append(task)
    except FileNotFoundError:
        print(f"Error!. File {file_path} not found")
    
    return task


