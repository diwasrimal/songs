import innertube

# Searches for a song and gives back their ids, thumbnails ..
def search_song(q):
    client = innertube.InnerTube("WEB")
    data = client.search(q)

    # Retrieve list of useful searches
    contents = (data['contents']['twoColumnSearchResultsRenderer']['primaryContents']
		    ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'])
    data = []

    # Loop through some portion of contents and collect info
    for i in range(len(contents)):

        try:
            videoContent = contents[i]["videoRenderer"]
        except KeyError:
            break

        thumbnail = videoContent["thumbnail"]["thumbnails"]
        data.append(
            {
                "id": videoContent["videoId"],
                # 'thumbnail': {
                # 	'url': thumbnail[0]['url'],
                # 	'width': thumbnail[0]['width'],
                # 	'height': thumbnail[0]['height']
                # },
                "thumbnail": thumbnail[0]["url"],
                "title": videoContent["title"]["runs"][0]["text"],
                "channel": videoContent["ownerText"]["runs"][0]["text"],
            }
        )

    return data


