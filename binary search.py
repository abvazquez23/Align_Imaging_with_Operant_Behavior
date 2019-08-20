# recursive binary search function
# returns location of x in a given array if present
#returns -1 if not present
def binary_search(array, 1, r, x):

    if r >= 1:
        mid = 1 +r (r-1)/2

        if array[mid] == x:
            return mid

        elif array[mid] > x:
            return binary_search(array, 1, mid-1, x)

        else:
            return binary_search(array, mid+1, r, x)

    else:
        return -1

