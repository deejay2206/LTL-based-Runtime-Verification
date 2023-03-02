import sys
import os

helpMessage = "Options:\n-i number_of_variables\t\tInitialise the model with variables.\n-a value1 value2 value3 ...\tAdd a new state to the model.\n-c -f property_file\t\tChecks a (e.g., FLTL) property forwards.\n-c -p property_file\t\tChecks a (e.g., PTLTL) property backwards.\n--help/-h\t\t\tDisplay help.\n"

def init(argv):
   try:         
      varnum = int(argv[2])
      mfile = open("model.csp", "w")
      for i in range(1, varnum + 1):
         mfile.write("var sv" + str(i) + ";\n")
      mfile.close()
   except:
      sys.exit("Can't initialise the model. Is the second argument an integer?")

def addNewState(argv):
   argnum = len(argv) - 2
   values = []
   for i in range(2, len(argv)):
      try:
         values.append(int(argv[i]))
      except:
         print("The argument is not an integer!")
   varnum = 0
   statenum = 0
   mfile = open("model.csp", "r")
   lines = mfile.readlines()
   mfile.close()
   for line in lines:
      if line.startswith("var"):
         varnum = varnum + 1
      if line.startswith("State"):
         statenum = statenum + 1
   if varnum != argnum:
      sys.exit("The number of arguments doesn't match the number of variables!")
   newstate = "State" + str(statenum + 1) + "() = s" + str(statenum + 1) + "{"
   for i in range(1, varnum + 1):
      newstate = newstate + "sv" + str(i) + " = " + str(values[i - 1]) + "; "
   newstate = newstate + "} -> Skip;\n"
   mfile = open("model.csp", "a")
   mfile.write(newstate)
   mfile.close()  

def getResult(filePath):
   file = open(filePath, "r")
   lines = file.readlines()
   if "NOT valid" in lines[3]:
      return False
   elif "VALID" in lines[3]:
      return True
   else:
      sys.exit("PAT result not parsed correctly.")

def check(argv):
   statenum = 0
   mfile = open("model.csp", "r")
   lines = mfile.readlines()
   mfile.close()
   for line in lines:
      if line.startswith("State"):
         statenum = statenum + 1
   trace = "Trace() = "
   if str(argv[2]) == "-f":         
      for i in range(1, statenum + 1):
         trace = trace + "State" + str(i) + "();"
   elif str(argv[2]) == "-p":
      for i in range(statenum, 0, -1):
         trace = trace + "State" + str(i) + "();"
   else:
      sys.exit("Unkonwn flag under -c!")
   trace = trace + "\n"
   lines.append(trace)
   pfile = open(str(argv[3]), "r")
   plines = pfile.readlines()
   pfile.close()
   tfile = open("tmp.csp", "w")
   tfile.writelines(lines)
   tfile.writelines(plines)
   tfile.close()
   # tfile = open("tmp2.nm", "w")
   # tfile.write("mc(\"tmp.csp\")")
   # tfile.close()
   os.system("cd .. && mono PAT3.Console.exe -nc runtime/tmp.csp runtime/result.txt")      
   # os.system("cd .. && cd .. && mono PAT351/PAT3.Console.exe ../NPAT-v1.0/runtime/tmp.csp ../NPAT-v1.0/runtime/result.txt")
   if getResult("result.txt"):
      print("PAT says yes.")
   else:
      print("PAT says no.")

if len(sys.argv) > 1:
   # Initialise the model.csp file with variables.
   # Format: program -i n (example: python3  runtime-monitor.py -i 4)
   #  where n is the number of variables. The default variable name is sv...
   if (str(sys.argv[1]) == "-i"): 
      init(sys.argv)           
   # Append a new state in model.csp.   
   # Format: program -a value1 value2 value3 ...
   elif str(sys.argv[1]) == "-a":
      addNewState(sys.argv)  
   # Runs PAT to check a FLTL or reachability property.   
   # Format: program -c -f file (python3 runtime-monitor.py -c -f  property.csp)
   #  where file contains the assertion to be checked.
   # ALTERNATIVELY Runs PAT to check a PTLTL property.   
   # Format: program -c -p file (python3 runtime-monitor.py -c -p  property.csp)
   #  where file contains the assertion to be checked.
   #  the syntax of PTLTL is the same as LTL but checks backwards in the past.
   #  X P checks P in the immediate previous state.
   #  <> P checks P in the previous sequence of states.
   #  [] P checks P in every previous state.
   #  P U Q is the same as P S Q in PTLTL.
   elif (len(sys.argv) > 3) & (str(sys.argv[1]) == "-c"):
      check(sys.argv)
   # Displays help message.
   elif (str(sys.argv[1]) == "--help") | (str(sys.argv[1]) == "-h"):
      print(helpMessage)
   else:
      print("Unknown/incomplete command!\n" + helpMessage)
