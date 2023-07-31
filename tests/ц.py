def func(nums):
    now = 0
    nex = 1
    tries = 0
    for num in nums:
        print(nums)
        print(tries)
        if num % 2 == 0:
            pass
        else:
            try:
                nums[now] += 1
                nums[nex] += 1
                tries += 1
            except IndexError:
                print('Не получится')
                return
        nex += 1
        now += 1
    print(tries)


func([1,2,3,4,5,6,7,8,9,12,10,3])


def make_even(nums):
    ops = 0
    for i in range(len(nums) - 1):
        if nums[i] % 2 == 1:
            nums[i + 1] += 1
            ops += 1

    return ops if len(nums) > 1 and nums[-1] % 2 == 0 else "impossible"

print(make_even([1,2,3,4,5,6,7,8,9,12,10,13]))