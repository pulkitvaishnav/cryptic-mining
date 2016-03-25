import re
#from django.core.serializers import json
import json
from django.http import HttpRequest, HttpResponse

whitedomain_list = ['127.0.0.1:8000', 'localhost:8000']
whitehost_list = ['127.0.0.1:8000', 'localhost:8000']
# making of CSM(compressed sparse matrix) from sparse matrix


def CSM(inputFile):  # = sys.argv[1]):
    CSM = [[0, 0, 0]]
    i = 0
    j = 0
    for line in inputFile:
        i += 1
        j = 0
        for word in line.split():
            j += 1
            if word != "0":
                CSM.append([i, j, word])

    CSM[0][0] = i  # total number of rows
    CSM[0][1] = j  # total number of columns
    CSM[0][2] = len(CSM) - 1  # total number of non-zero elements
    return CSM


# reforming sparse matrix from CSM
def sparseMatrix(CSM):
    p = 1
    for i in xrange(CSM[0][0]):
        for j in xrange(CSM[0][1]):
            if p <= CSM[0][2] and i == CSM[p][0] - 1 and j == CSM[p][1] - 1:
                print CSM[p][2],
                p += 1
            else:
                print 0,
        print "\n"


def decrypt_linear(i, j, word):
    old_word = ""
    for char in word.split('-'):
        old_word += chr((int(char) - i) / j)
    return old_word


def decrypt_quadratic(i, j, word):
    old_word = ""
    for char in word.split('-'):
        old_word += chr((int(char) - i) / (j + (i + j)**2))
    return old_word


def decrypt_cubic(i, j, word):
    old_word = ""
    for char in word.split('-'):
        old_word += chr((int(char) - i) / (j + (i + j)**2 + (i + j)**3))
    return old_word


def encrypt_linear(i, j, word):
    new_word = ""
    for char in word:
        new_word = new_word + '-' + str(i + j * ord(char))
    return new_word[1:]


def encrypt_quadratic(i, j, word):
    new_word = ""
    for char in word:
        new_word = new_word + '-' + str(i + (j + (i + j)**2) * ord(char))
    # print decrypt(i,j,new_word[1:])
    return new_word[1:]


def encrypt_cubic(i, j, word):
    new_word = ""
    for char in word:
        new_word = new_word + '-' + \
            str(i + (j + (i + j)**2 + (i + j)**3) * ord(char))
    return new_word[1:]


def encrypt_CSM_linear(inputFile):  # = sys.argv[1]):
    CSM = [[0, 0, 0]]
    i = 0
    
    for line in inputFile:
        i += 1
        j = 0
        for word in line.split():
            j += 1
            if word != "0":
                encrypt_word = encrypt_linear(i, j, word)
                CSM.append([i, j, encrypt_word])

    CSM[0][0] = i  # total number of rows
    CSM[0][1] = j  # total number of columns
    CSM[0][2] = len(CSM) - 1  # total number of non-zero elements
    return CSM


def encrypt_CSM_quadratic(inputFile):  # = sys.argv[1]):
    CSM = [[0, 0, 0]]
    i = 0
    for line in inputFile:
        i += 1
        j = 0
        for word in line.split():
            j += 1
            if word != "0":
                encrypt_word = encrypt_quadratic(i, j, word)
                CSM.append([i, j, encrypt_word])

    CSM[0][0] = i  # total number of rows
    CSM[0][1] = j  # total number of columns
    CSM[0][2] = len(CSM) - 1  # total number of non-zero elements
    return CSM


def encrypt_CSM_cubic(inputFile):  # = sys.argv[1]):
    CSM = [[0, 0, 0]]
    i = 0
    for line in inputFile:
        i += 1
        j = 0
        for word in line.split():
            j += 1
            if word != "0":
                encrypt_word = encrypt_cubic(i, j, word)
                CSM.append([i, j, encrypt_word])

    CSM[0][0] = i  # total number of rows
    CSM[0][1] = j  # total number of columns
    CSM[0][2] = len(CSM) - 1  # total number of non-zero elements
    return CSM


def decrypt_CSM_linear(encrypted_CSM):
    for i in encrypted_CSM[1:]:
        i[2] = decrypt_linear(i[0], i[1], i[2])
    return encrypted_CSM


def decrypt_CSM_quadratic(encrypted_CSM):
    for i in encrypted_CSM[1:]:
        i[2] = decrypt_quadratic(i[0], i[1], i[2])
    return encrypted_CSM


def decrypt_CSM_cubic(encrypted_CSM):
    for i in encrypted_CSM[1:]:
        i[2] = decrypt_cubic(i[0], i[1], i[2])
    return encrypted_CSM




def set_response_header(**kwargs):
    # pdb.set_trace()
    pattern = re.compile("^chrome-extension://*")
    if isinstance(kwargs['request'], HttpRequest) and isinstance(kwargs['response'], HttpResponse):
        if kwargs['request'].META.has_key('HTTP_ORIGIN') and kwargs['request'].META['HTTP_ORIGIN'] in whitedomain_list:
            kwargs['response']['Access-Control-Allow-Credentials'] = 'true'
            kwargs['response'][
                'Access-Control-Allow-Methods'] = "GET, POST, OPTIONS, DELETE, PUT"
            kwargs['response']['Access-Control-Allow-Origin'] = "*"
            #kwargs['response']['Access-Control-Allow-Origin']="http://web-staging.flyrobeapp.com/, http://localhost:8000/"
            kwargs['response']['Access-Control-Max-Age'] = "1728000"
            kwargs['response'][
                'Cache-Control'] = "max-age=0, private, must-revalidate"
            kwargs['response'].__delitem__("X-Frame-Options")
            return True, kwargs['response']
        elif kwargs['request'].META.has_key('HTTP_ORIGIN') and pattern.match(kwargs['request'].META['HTTP_ORIGIN']):
            return True, kwargs['response']
        elif kwargs['request'].META.has_key('HTTP_HOST') and kwargs['request'].META['HTTP_HOST'] in whitehost_list:
            kwargs['response']['Access-Control-Allow-Credentials'] = 'true'
            kwargs['response'][
                'Access-Control-Allow-Methods'] = "GET, POST, OPTIONS, DELETE, PUT"
            kwargs['response']['Access-Control-Allow-Origin'] = "*"
            #kwargs['response']['Access-Control-Allow-Origin']="http://web-staging.flyrobeapp.com/, http://localhost:8000/"
            kwargs['response']['Access-Control-Max-Age'] = "1728000"
            kwargs['response'][
                'Cache-Control'] = "max-age=0, private, must-revalidate"
            kwargs['response'].__delitem__("X-Frame-Options")
            return True, kwargs['response']
        elif not kwargs['request'].META.has_key('HTTP_ORIGIN') and not kwargs['request'].META.has_key('HTTP_HOST'):
            return True, kwargs['response']
    else:
        return False, kwargs['response']


class JsonResponse(HttpResponse):
    '''
    Handling content type for json no more to add content-type.
    '''

    def __init__(self, content={}, status=None, content_type='application/json'):
        super(JsonResponse, self).__init__(
            json.json.dumps(content), status=status, content_type=content_type)
