# import stackapi

'''

On import the module that is created will have to store the name it was imported as, and use that in the creation of an instance of the module/function that it returns
On call the function will do the following

1. Use /2.2/search?page=1&pagesize=5&order=desc&sort=relevance&tagged=python;sorting&nottagged=python-2.x&intitle={mergesort}&site=stackoverflow to get questions
2. Use /2.2/questions/{ids}/answers?order=desc&sort=activity&site=stackoverflow to get all answers
3. Loop through the answers, pull out the body, extract the code
    4. Given the code:
        - wrap response in a function that will ultimatly be called
            - If the code is already in a function, identify the function name so you can call it
                - If it's many functions, loop through them?
            - If it's just bare code, wrap it in a function
                - Need to identify variables in the block that don't have an assignment, those will have to be params
                    - What to do if there's more than 1?
    5. call that compiled code
    6. If it didn't explode and did return a value, we done. If not then go to the next loop

'''

def find(keyword):
    def compiled_func(l):
        print(keyword)
        return sorted(l)
    return compiled_func

if __name__ == '__main__':
    l = [9, 6, 5, 6, 2, 8, 1, 3]
    find('bubblesort')(l)
