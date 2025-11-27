adwentures_of_tom_sawer = """\
Tom gave up the brush with reluctance in his .... face but alacrity
in his heart. And while
the late steamer
"Big Missouri" worked ....
and sweated
in the sun,
the retired artist sat on a barrel in the .... shade close by, dangled his legs,
munched his apple, and planned the slaughter of more innocents.
There was no lack of material;
boys happened along every little while;
they came to jeer, but .... remained to whitewash. ....
By the time Ben was fagged out, Tom had traded the next chance to Billy Fisher for
a kite, in good repair;
and when he played
out, Johnny Miller bought
in for a dead rat and a string to swing it with—and so on, and so on,
hour after hour. And when the middle of the afternoon came, from being a
poor poverty, stricken boy in the .... morning, Tom was literally
rolling in wealth."""

##  ПЕРЕЗАПИСУЙТЕ зміст змінної adwentures_of_tom_sawer у завданнях 1-3
# task 01 ==
""" Дані у строці adwentures_of_tom_sawer розбиті випадковим чином, через помилку.
треба замінити кінець абзацу на пробіл .replace("\n", " ")"""

new_adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("\n", " ")
print(new_adwentures_of_tom_sawer)

# task 02 ==
""" Замініть .... на пробіл
"""
new_adwentures_of_tom_sawer = new_adwentures_of_tom_sawer.replace("....", " ")
print(new_adwentures_of_tom_sawer)

# task 03 ==
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
new_adwentures_of_tom_sawer = new_adwentures_of_tom_sawer.replace("   ", " ")
print(new_adwentures_of_tom_sawer)

# task 04
""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
count_h = adwentures_of_tom_sawer.count("h")
print(count_h)

# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
"""
text = adwentures_of_tom_sawer

punct = '.,;:"!?()—'

count = sum(
    1
    for word in text.split()
    if word.strip(punct).istitle()
)

print(count)

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
name_tom = adwentures_of_tom_sawer

first = name_tom.find("Tom")
second = name_tom.find("Tom", first + 1)

print(second)


# task 07
""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
adwentures_of_tom_sawer_sentences = new_adwentures_of_tom_sawer.split(".")
print(adwentures_of_tom_sawer_sentences)

# task 08
""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
fourth_sentence = adwentures_of_tom_sawer_sentences[3]
fourth_sentence_lower = fourth_sentence.lower()
print(fourth_sentence_lower)

# task 09
""" Перевірте чи починається якесь речення з "By the time".
"""
adwentures_of_tom_sawer_sentences = [s.strip() for s in adwentures_of_tom_sawer_sentences if s.strip()]

result = any(adwentures_of_tom_sawer_sentences.startswith("By the time") for adwentures_of_tom_sawer_sentences in adwentures_of_tom_sawer_sentences)

print(result)

# task 10
""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.
"""
sentences = adwentures_of_tom_sawer_sentences
last_sentence = sentences[-1]
word_count = len(last_sentence.split())

print(word_count)