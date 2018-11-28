from pathlib import Path
import os, time, subprocess, requests
from bs4 import BeautifulSoup

code = lang = filename = None


def scrape(url):
    global code, lang, filename

    url = requests.get(url, headers = {'User-Agent' : "Mozilla/5.0"})
    parser = BeautifulSoup(url.text, "lxml")

    code = parser.find_all("pre")[0]
    code = BeautifulSoup(str(code), "lxml").text

    lang = parser.find_all("td")[3]
    lang = BeautifulSoup(str(lang), "lxml").text.strip().lower()

    for iterator in parser.select("td")[14]:
        filename = iterator.attrs['value']
        break


def saveToFile(fileLocation, contents, mode = "w+"):
    file = open(fileLocation, mode)
    file.write(contents)
    file.close()


def execute(command, inputFileLoc = None, outputFileLoc = None):
    if inputFileLoc is not None:
        command = command + " < " + inputFileLoc
    if outputFileLoc is not None:
        command = command + " > " + outputFileLoc
    print(command)
    process = subprocess.run(command, shell = True, cwd = "/")
    if process.returncode != 0:
        raise Exception


def runCode(dirLocation, filename, lang, inputFileLoc, outputFileLoc, skipCompiling = 0):
    lang = lang.lower()
    fileLocation = dirLocation + "/" + filename

    if 'java' in lang:
        if not skipCompiling:
            execute("javac " + fileLocation)
        execute("java -cp " + dirLocation + " " + filename[0 : -5],
                inputFileLoc, outputFileLoc)

    elif 'c++' in lang or 'cpp' in lang:
        cppExecutable = dirLocation + '/' + filename[0 : -4]
        if not skipCompiling:
            execute("g++ -o " + cppExecutable + " -O2 -std=c++14 " + fileLocation)
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


def matchOutputs(output, answer):
    output = output.split()
    answer = answer.split()
    return output == answer


desktopPath = str(Path.home()) + "/Desktop"

def hack_it(solutionID, problemCode):
    scrapeUrl = "https://codeforces.com/contest/1076/submission/" + solutionID

    dirLocation = desktopPath + "/" + problemCode
    hackInfoFile = desktopPath + "/Hackable"
    inputFileLoc = dirLocation + "/input"
    outputFileLoc = dirLocation + "/output"
    answerLocation = dirLocation + "/answer"

    scrape(scrapeUrl)
    fileLocation = dirLocation + '/' + filename
    saveToFile(fileLocation, code)

    #print(code)
    #print(lang)
    #print(filename)



    for i in range(70):
        runCode(dirLocation, "gen.py", "python", None, inputFileLoc)
        runCode(dirLocation, "ActualSolution.cpp", "c++", inputFileLoc, answerLocation, True)
        try:
            runCode(dirLocation, filename, lang, inputFileLoc, outputFileLoc, i)
            outputContents = readFromFile(outputFileLoc)
            answerContents = readFromFile(answerLocation)
            if not matchOutputs(outputContents, answerContents):
                1/0
            print ("Passed")
        except:
            print ("Try hacking " + solutionID)
            #print (readFromFile(inputFileLoc))
            saveToFile(hackInfoFile + "/" + solutionID, readFromFile(inputFileLoc))
            break


    if os.path.exists(dirLocation + "/" + filename):
        os.remove(dirLocation + "/" + filename)
    if os.path.exists(dirLocation + "/" + filename[0 : -5] + ".class"):
        os.remove(dirLocation + "/" + filename[0 : -5] + ".class")
    if os.path.exists(dirLocation + "/" + filename[0 : -4]):
        os.remove(dirLocation + "/" + filename[0 : -4])

    if os.path.exists(inputFileLoc):
        os.remove(inputFileLoc)
    if os.path.exists(outputFileLoc):
        os.remove(outputFileLoc)
    if os.path.exists(answerLocation):
        os.remove(answerLocation)


last = 0
while True:
    ids = readFromFile(desktopPath + "/acceptedIDs").split("\n")
    while len(ids[-1]) < 2:
        ids.pop()
    try:
        if last >= len(ids):
            print ("Waiting for new IDs...")
            time.sleep(1)
        while last < len(ids):
            solutionDetails = ids[last].split()
            hack_it(solutionDetails[0], chr(int(solutionDetails[1]) + ord("A")))
            last += 1
    except:
        pass
        print ("Error encountered while parsing accepted IDs...")
