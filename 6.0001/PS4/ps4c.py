from ps4a import get_permutations

### HELPER CODE ###


def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''

    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    # >>> is_word(word_list, 'bat') returns
    # True
    # >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        word_list = load_words(WORDLIST_FILENAME)
        self.text = text
        self.valid_words = []
        copy_words = list(self.text.split(" "))
        for word in copy_words:
            if is_word(word_list, word):
                self.valid_words.append(word)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy_valid_words = self.valid_words.copy()
        return copy_valid_words

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        transpose_dict = {}
        vowels_lower = 'aeiou'
        vowels_upper = 'AEIOU'
        consonants_lower = 'bcdfghjklmnpqrstvwxyz'
        consonants_upper = 'BCDFGHJKLMNPQRSTVWXYZ'

        # Map the lowercase vowels according to the permutation
        for i in range(len(vowels_lower)):
            transpose_dict[vowels_lower[i]] = vowels_permutation[i]

        # Map the uppercase vowels according to the permutation
        for i in range(len(vowels_upper)):
            transpose_dict[vowels_upper[i]] = vowels_permutation[i].upper()

        # Map the lowercase consonants to themselves
        for letter in consonants_lower:
            transpose_dict[letter] = letter

        for letter in consonants_upper:
            transpose_dict[letter] = letter
        return transpose_dict

    def apply_transpose(self, transpose_dict):
        """
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        """
        encrypted_message = ""
        for letter in self.get_message_text():
            if letter in transpose_dict:
                # Check if the letter is uppercase
                if letter.isupper():
                    # If the letter is uppercase, use the uppercase version of the cipher letter
                    encrypted_message += transpose_dict[letter.lower()].upper()
                else:
                    encrypted_message += transpose_dict[letter]
            else:
                # If the letter is not in the transpose dictionary, it must be a consonant
                # In that case, use the original letter
                encrypted_message += letter
        return encrypted_message


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)
        self.message_text = text
        self.valid_words = []
        copy_words = list(self.message_text.split(" "))
        word_list = load_words(WORDLIST_FILENAME)
        for word in copy_words:
            if is_word(word_list, word):
                self.valid_words.append(word)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message
        '''

        word_list = load_words(WORDLIST_FILENAME)

        max_valid_words = 0
        best_decrypted_text = None

        for permutation in get_permutations('aeiou'):
            transpose_dict = self.build_transpose_dict(permutation)
            decrypted_text = self.apply_transpose(transpose_dict)
            decrypted_words = decrypted_text.split()
            valid_words = 0

            for word in decrypted_words:
                if is_word(word_list, word):
                    valid_words += 1

            if valid_words > max_valid_words:
                max_valid_words = valid_words
                best_decrypted_text = decrypted_text  # update best_decrypted_text here

        if max_valid_words == 0:
            return self.get_message_text()
        else:
            return best_decrypted_text  # return best_decrypted_text here

    def get_permutations(self, text):
        permutations = []
        valid_word = None

        if len(text) == 1:
            return [text]
        else:
            for char in text:
                [permutations.append(char + a) for a in get_permutations(text.replace(char, "", 1))]

        for permutation in permutations:
            if permutation in self.valid_words:
                valid_word += permutation
            else:
                continue

        if not valid_word:
            return self.message_text
        else:
            return valid_word


if __name__ == '__main__':
    print("test")
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))

    message = EncryptedSubMessage("Hollu Wurld!")
    permutation = "zyxwv"
    expected_output = "Hello World!"
    print("Original encrypted message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected decryption:", expected_output)
    print("Actual decryption:", message.decrypt_message())
