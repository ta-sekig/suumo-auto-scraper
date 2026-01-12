base_url = "https://example.com/items?page="

for page_number in range(1, 6):
    target_url = base_url + str(page_number)
    print(f"{page_number}ページ目のURL:{target_url}")
    print("----------------------")

   