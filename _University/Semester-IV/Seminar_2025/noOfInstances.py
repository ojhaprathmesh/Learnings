def max_instances(text: str) -> int:
    word = "balloon"
    char_count = {char: text.count(char) for char in word}
    required = {char: word.count(char) for char in word}

    return min(char_count.get(char, 0) // required[char] for char in required)

# Test cases (Checking how many times "balloon" can be formed)
print(max_instances("bcadeaglkmpooglooo"))
print(max_instances("balloonballoonballoon"))
print(max_instances("baeeobbboonlaloloaln"))
