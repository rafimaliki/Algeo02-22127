import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, max_images):

    # Request HTML
    response = requests.get(url)
    folder_path = "website/static/dataset_picture"

    # Cek apakah request berhasil
    if response.status_code == 200:

        # Parsing HTML menggunakan Beautiful Soup
        parsed = BeautifulSoup(response.text, 'html.parser')

        # Cari tag <img>
        img_tags = parsed.find_all('img')

        count = len(os.listdir('website/static/dataset_picture'))
        max_images = count + max_images

        google_logo = True

        # Download image
        for img_tag in img_tags:

            # Skip foto pertama karena biasanya logo google
            if google_logo:
                google_logo = False
                continue

            if max_images is not None and count >= max_images:
                break

            try:

                # Cari link dari atribut src
                img_url = img_tag.get('src')
                if img_url:
                    
                    # Melengkapi url img
                    img_url = urljoin(url, img_url)
                    
                    # Request binary data img dari url
                    img_data = requests.get(img_url).content
                
                    count += 1
                    img_name = os.path.join(folder_path, f'{count}.jpg')
                    
                    # Save binary data img ke folder
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_data)

                    print(f"Downloaded: {img_name}")
            except:
                print("Fail to download image")
    else:
        print("Fail to get HTML")