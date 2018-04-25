
import aiml
import os
path = 'C:/Users/hp/Documents/Python Scripts/AIC'
brain_file = "QA.brn"
os.chdir(path)



if __name__ == '__main__':
    kern = aiml.Kernel()
    kern.bootstrap(learnFiles=path+'/QA.xml', commands="load aiml b")
    kern.saveBrain(brain_file)
    kern.bootstrap(brainFile = brain_file)
    while True:
        print (kern.respond(input()))
