from web_connect import Translator as ken

TEXT = """
Hello, how are you?
Have you been alright through all those lonely
Lonely, lonely, lonely, lonely nights?
That's what I'd say, I'd tell you everything
If you pick up that telephone, yeah, yeah, yeah
Hey, how you feelin'?
Are you still the same, don't you realize the things we did
We did were all for real, not a dream
I just can't believe they've all faded out
Of view, yeah, yeah, yeah, yeah, ooh
Blue days, black nights
I look into the sky (the love you need ain't gonna see you through)
And I wonder why (the little things you planned ain't comin' true)
Oh, oh, telephone line, give me some time, I'm living in twilight
Oh, oh, telephone line, give me some time, I'm living in twilight
Okay, so no one's answering
Well, can't you just let it ring a little longer
Longer, longer oh, I'll just sit tight
Through shadows of the night
Let it ring forever more, oh
Blue days, black nights, doo wah doo lang
I look into the sky (the love you need ain't gonna see you through)
And I wonder why (the little things you planned ain't comin' true)
Oh, oh, telephone line, give me some time, I'm living in twilight
Oh, oh, telephone line, give me some time, I'm living in twilight
Oh, oh, telephone line, give me some time, I'm living in twilight
Oh, oh, telephone line, give me some time, I'm living in twilight
"""

"""
translate_text
    This function translates a small bit of text
    :param text, iterations
    text-Text that will be translated
    iterations-Number of times the text will be sent through google translate.
        !NOTE! Since the text will be translated back into English at the end, 
                the number of times that the text will be translated is iterations + 1
"""
def translate_text(text="", iterations=20):
    if len(text.split()) > 500:
        print("Text is too long. Maximum word count is 500 words. Place the text in a text file to translate")
        return ""
    print("Starting up")
    return ken().translate(text, iterations)


"""
translate_file
    This function translates an entire text file in sections of 500 words
    
    :param file, iterations
    file-Text file that will be translated
    iterations-Number of times the file will be sent through google translate.
        !NOTE! Since the file will be translated back into English at the end, 
                the number of times that the file will be translated is iterations + 1
"""
def translate_file(file=None, iterations=20):
    text = ""
    count = 0
    output = open("Output_file.txt", 'w')
    with open(file, 'r') as file:
        # This creates a buffer. The text file is read in as <500 word sections at
        # a time so as to not overload google translate and cause problems.
        for line in file:
            if count + len(line.split()) < 500:
                text += line
                count += len(line.split())
            # After a <500 word section has been created, we translate that section,
            # restart the counter and start again
            else:
                write_to_output(output, text, iterations)
                text = ""
                count = 0
    # This section writes out the last section that didn't reach 500 words
    write_to_output(output, text, iterations)


"""
write_to_output
    :param file, text, iterations
    file-Text file to write to
    text-Text to translate
    iterations-Number of times the translation program runs
"""
def write_to_output(file, text, iterations):
    again = True
    while again:
        again = False
        try:
            file.write(translate_text(text, iterations))
        except UnicodeEncodeError:
            # Sometimes the translation back into English fails because
            # google translate doesn't know how to map certain characters.
            # Due to the random nature of this program, there isn't an easy way
            # of preventing this, so we just rerun the whole translation
            print("Invalid character found, running translation again")
            again = True


def main():
    TEXT=input("Type in text: ")
    print(translate_text(text=TEXT))


if __name__ == "__main__":
    main()
