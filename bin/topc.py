from TopCompiler import topc
from TopCompiler import Error
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:

        if sys.argv[1] == "new":
            if sys.argv[2] == "project":
                topc.newProj(sys.argv[3])
            elif sys.argv[2] == "package":
                topc.newPack(sys.argv[3])
            elif sys.argv[2] == "linkWith":
                topc.linkWith(sys.argv[3])
            else:
                Error.error("invalid option to new"+sys.argv[2])
            sys.exit()
        elif sys.argv[1] == "build":
            topc.start()
        elif sys.argv[1] == "run":
            topc.start(True)
        else:
            Error.error("invalid option "+sys.argv[1])