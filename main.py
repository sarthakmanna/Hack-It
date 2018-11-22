import subprocess, requests
from bs4 import BeautifulSoup

dirLocation = "/home/sarthakmanna/Desktop"

code = lang = filename = None


def scrape(url):
    global code, lang, filename, dirLocation

    url = requests.get(url, headers = {'User-Agent' : "Mozilla/5.0"})
    parser = BeautifulSoup(url.text, "lxml")

    code = parser.find_all("pre")[0]
    code = BeautifulSoup(str(code), "lxml").text

    lang = parser.find_all("td")[3]
    lang = BeautifulSoup(str(lang), "lxml").text.strip().lower()

    for iterator in parser.select("td")[14]:
        filename = iterator.attrs['value']
        break


def saveToFile(fileLocation, contents):
    file = open(fileLocation, "w")
    file.write(contents)
    file.close()


def compile(command):
    print(command)
    process = subprocess.Popen(command.split(), cwd = '/')
    process.wait()


def execute(command, inputFileLoc, outputFileLoc):
    arg = command + " < " + inputFileLoc + " > " + outputFileLoc
    print(arg)
    process = subprocess.run(arg, shell = True, cwd = "/")
    if process.returncode != 0:
        raise Exception


inputFileLoc = "/home/sarthakmanna/Desktop/input.txt"
outputFileLoc = "/home/sarthakmanna/Desktop/output.txt"
answerLocation = "/home/sarthakmanna/Desktop/answer.txt"

scrape("http://codeforces.com/contest/1061/submission/46065597")
fileLocation = dirLocation + '/' + filename
saveToFile(fileLocation, code)

#print(code)
print(lang)
print(filename)

if 'java' in lang:
    compile("javac " + fileLocation)
    execute("java -cp " + dirLocation + " " + filename[0 : -5],
            inputFileLoc, outputFileLoc)
elif 'c++' in lang:
    cppExecutable = dirLocation + '/' + filename[0 : -4]
    compile("g++ -o " + cppExecutable + " -O2 -std=c++14 " + fileLocation)
    execute("." + cppExecutable, inputFileLoc, outputFileLoc)
elif "py" in lang:
    pyExecutable = fileLocation
    try:
        execute("python2 " + pyExecutable, inputFileLoc, outputFileLoc)
    except:
        try:
            execute("python3 " + pyExecutable, inputFileLoc, outputFileLoc)
        except:
            try:
                execute("python " + pyExecutable, inputFileLoc, outputFileLoc)
            except:
                pass


def readFromFile(fileLocation):
    file = open(fileLocation, "r")
    contents = ''.join(file.readlines())
    file.close()
    return contents


def checkOutput(output, answer):
    output = output.split()
    answer = answer.split()
    return output == answer


outputContents = readFromFile(outputFileLoc)
answerContents = readFromFile(answerLocation)
print(checkOutput(outputContents, answerContents))
