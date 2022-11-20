#CREDITS/THANKS
#https://stackoverflow.com/questions/37921295/python-pil-image-make-3x3-grid-from-sequence-images
#https://thecleverprogrammer.com/2021/06/08/convert-image-to-array-using-python/
#https://thecleverprogrammer.com/2021/07/31/collage-maker-using-python/
#https://anilist.gitbook.io/anilist-apiv2-docs/overview/graphql/getting-started
#https://anilist.github.io/ApiV2-GraphQL-Docs/
#https://github.com/walfie/anime-bingo
#https://stackoverflow.com/questions/9029287/how-to-extract-http-response-body-from-a-python-requests-call
#https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
#https://pythonbasics.org/read-excel/
#https://www.geeksforgeeks.org/how-to-convert-pandas-dataframe-into-a-list/
#https://auth0.com/blog/image-processing-in-python-with-pillow/
#https://code-maven.com/create-images-with-python-pil-pillow
#https://stackoverflow.com/questions/24085996/how-i-can-load-a-font-file-with-pil-imagefont-truetype-without-specifying-the-ab
#https://www.programcreek.com/python/?CodeExample=draw+rectangle
#https://www.blog.pythonlibrary.org/2021/02/23/drawing-shapes-on-images-with-python-and-pillow/
#https://pillow.readthedocs.io/en/stable/reference/ImageFont.html

from PIL import Image, ImageDraw, ImageFont
import requests
from time import sleep
import pandas as pd

images = [[]] # n image groups
numberRows, numberCols = 2, 2
globalCounter = 1
archiveName = "P.xlsx"

def read_images(sheet_number):
    global globalCounter
    imagesExcel = pd.read_excel(archiveName, sheet_name = sheet_number)['Id_Anilist'].tolist()
    imagesListReturn = {'images':[],'names':[]}
    for i,image in enumerate(imagesExcel):
        query = '''
            query ($id: Int) {
              Character (id: $id) {
                name {full}
                image {medium}
              }
            }
        '''
        ids = {
            'id': image
        }
        request = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': ids})
        response = request.json()
        imagesListReturn['images'].append(Image.open(requests.get(response['data']['Character']['image']['medium'], stream=True).raw))        
        imagesListReturn['names'].append(response['data']['Character']['name']['full'])
        request.close()
        sleep(8)
        print(globalCounter) if globalCounter % numberRows == 0 else 0
        globalCounter += 1 
    return imagesListReturn

def image_grid(imgs, names, rows, cols):
    assert len(imgs) == rows*cols
    w, h = 230, 358
    fnt = ImageFont.truetype('arial.ttf', 12)
    grid = Image.new('RGB', size=(cols*w, rows*h))
    for i, img in enumerate(imgs):
        nameLength = fnt.getlength(names[i])
        img = img.resize((w,h))
        draw = ImageDraw.Draw(img)
        draw.rectangle((w/2-nameLength/2-10,h-5,w/2-nameLength/2+nameLength+10,h-25),(250,250,250))
        draw.text((w/2-nameLength/2,h-20), names[i], fill=(50,50,50),font=fnt)
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

for i,group in enumerate(images):
    group = read_images(i)
    image_grid(group['images'],group['names'], rows = numberRows, cols = numberCols).save(f'grid{i+1}.jpg')
