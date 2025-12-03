import json
def get_programs():
    with open('programs.json', 'r') as archivo:
        programs = json.load(archivo)

    program_list = [element.lower() if isinstance(element, str) else element
                    for element in programs["programs_list"]]
    return  program_list

if __name__ == "__main__":
    result = get_programs()
    print(result)