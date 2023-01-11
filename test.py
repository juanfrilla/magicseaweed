mydict = {
    "url": "www",
    "beach": "Famara",
    "island": "Lanzarote"
}

for element in list(mydict.items())[1:]:
    print(element[0])