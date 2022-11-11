import subprocess


def execute(script: str) -> str:
	output = subprocess.check_output(["python", "-c", script]).decode("utf-8").strip()
	return output


if __name__ == '__main__':
	output = execute("""
def solution(n, arr1, arr2):
    pattern = [' ', '#']
    result = []
    for i in range(n) :
        decoded = ''
        union = arr1[i] | arr2[i]
        for _ in range(n):
            decoded = pattern[union % 2] + decoded
            union //= 2
        result.append(decoded)
    
    return result


if __name__ == '__main__':
    result = solution(
        6,
        [46, 33, 33 ,22, 31, 50],
        [27 ,56, 19, 14, 14, 10]
    )
    print(result)
    print(result)
""")
	# 결과는 무조건 str으로 출력됨.
	print(output)
	print(type(output))
	# 복수의 개행 문자의 경우, \n으로 오며, 아래와 같이 split()로 다룰 수도 있음.
	print(output.split("\n"))
	
