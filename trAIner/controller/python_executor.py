import subprocess
from subprocess import TimeoutExpired


def execute(script: str, input_str: str, timeout: int = 10) -> str:
	"""Execute the given script with the given input and return the output."""
	output = subprocess.run(
		["python3", "-c", script],
		input=input_str,
		capture_output=True,
		encoding="utf-8",
		timeout=timeout,
	)
	return output.stdout


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
	
