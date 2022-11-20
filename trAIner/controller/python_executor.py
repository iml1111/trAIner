import subprocess
from time import time
from subprocess import TimeoutExpired, CalledProcessError


def execute(script: str, input_str: str, timeout: int = 10) -> str:
	"""Execute the given script with the given input and return the output."""
	output = subprocess.run(
		["python", "-c", script],
		input=input_str,
		capture_output=True,
		encoding="utf-8",
		timeout=timeout,
	)
	return output.stdout


def run_problem(code: str, input_str: str, output_str: str, timeout: int = 10):
    process_time = None
    try:
        process_time = time()
        data = execute(code, input_str, timeout)
        process_time = time() - process_time
        if data == output_str:
            result = True
            description = "맞았습니다!!"
        else:
            result = False
            description = "틀렸습니다!!"
    except CalledProcessError:
        result = False
        description = '런타임 에러'
    except TimeoutExpired:
        result = False
        description = '시간 초과'

    print(data.encode('utf-8'))
    print(output_str.encode('utf-8'))
    return {
        'result': result,
        'description': description,
        'time': process_time if process_time else None
    }


if __name__ == '__main__':
	output = execute("""
input_str = input()
input_str2 = input()

int1, int2 = input_str.split()
int1, int2 = int(int1), int(int2)
print(int1 + int2)
print(input_str2.split())
""", "1 2\nasd asd")
	print(output, type(output))
