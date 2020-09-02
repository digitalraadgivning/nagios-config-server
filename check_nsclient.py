import requests, json, base64, sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

(EXIT_OK, EXIT_WARNING, EXIT_CRITICAL, EXIT_UNKNOWN) = (0,1,2,3)

def main():
    try:
        #Check if correct parameters are entered


        if len(sys.argv) < 6:
            print("Syntax error! The syntax is: [server_address] [port] [username] [password] [command] [arguments]")
            sys.exit(EXIT_UNKNOWN)


        status,message,perfs = FetchAndParse(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5:])

        status_message = message

        if(len(perfs)>0):
            status_message += ' - '

        for perf in perfs:
            values = perfs[perf]

            status_message += perf + ": " + str(int(values["value"])) +  str(values["unit"]) + ", "

        status_message = status_message[:-2]

        if(len(perfs)>0):
            status_message += " - warn/crit: "

        for perf in perfs:
            values = perfs[perf]
            status_message += str(int(values["warning"])) +  str(values["unit"]) + "/" + str(int(values["critical"])) +  str(values["unit"]) + ", "

        status_message = status_message[:-2]

        print(status_message)

        if status == "OK" or status == EXIT_OK:
            sys.exit(EXIT_OK)
        elif status == "WARNING" or status == EXIT_WARNING:
            sys.exit(EXIT_WARNING)
        elif status == "CRITICAL" or status == EXIT_CRITICAL:
            sys.exit(EXIT_CRITICAL)
        elif status == "UNKNOWN" or status == EXIT_UNKNOWN:
            sys.exit(EXIT_UNKNOWN)
        else:
            print("Exit code error. Status is not set to a valid exit code")
            sys.exit(EXIT_UNKNOWN)

    except Exception as e:
        print("Error in main()")
        print (str(e))
        sys.exit(EXIT_UNKNOWN)



def SetUrl(srv_address, port, commands):

    url = "https://" + str(srv_address) + ":" + str(port) + "/api/v1/queries/" + commands[0] + "/commands/execute"

    if(len(commands[1:]) > 0):
        url += "?"
        for argument in commands[1:]:
            url += argument + "&"
        url = url[:-1]

    return url


def FetchAndParse(srv_address, port, user, password, commands):
    response = ""
    try:
        response = requests.get(SetUrl(srv_address, port, commands), auth=(user, password), verify=False)
        data = response.json()

        message = data["lines"][0]["message"]
        perfs = data["lines"][0]["perf"]
        status = data["result"]

        return status,message,perfs

    except Exception as e:
            print ("Error in FetchAndParse(): ", str(e))
            print (response)
            sys.exit(EXIT_UNKNOWN)

if __name__ == "__main__":
    main()
