
def loadTask(file_path):
    tasks=[]

    try:
        with open(file_path,"r") as file:
            for line in file:
                task= line.strip()
                if task:
                    tasks.append(task)
    except FileNotFoundError:
        print(f"Error!. File {file_path} not found")
    
    return tasks

tasker=loadTask("data/testData.txt")
print("Loaded tasks: ")
for t in tasker:
     print(t)




