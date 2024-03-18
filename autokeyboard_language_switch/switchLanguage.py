from language_funcs import switchStringLanguage
import sys

if __name__ == "__main__":
   
    string = sys.stdin.readline().replace('\n', '')

    string = bytes.fromhex(string).decode("utf-16")[:-1]

    output = switchStringLanguage(string)        
    
    sys.stdout.writelines(output.encode("utf-16").hex()[4:]+ "0000" + "\n")
    sys.stdout.flush()
