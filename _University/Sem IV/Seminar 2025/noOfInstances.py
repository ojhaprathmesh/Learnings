def max_instances(text: str) -> int:
    word = "balloon"
    char_count = {char: text.count(char) for char in word}
    required = {char: word.count(char) for char in word}

    return min(char_count.get(char, 0) // required[char] for char in required)

# Test cases
print(max_instances("bcadeaglkmpoogl"))
print(max_instances("balloon"))
print(max_instances("baeeobbboonlaloloaln"))
