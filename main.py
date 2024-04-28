import getImageData
import handRankings

from flask import Flask, jsonify, request
from flask_cors import CORS 

import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/get_card_data', methods=['POST'])
def getCardData():
    data = request.json
    imageReqData = data.get('image')
    imageDataCode = imageReqData.split(',')[1]
    imageBytes = base64.b64decode(imageDataCode)
    image = Image.open(BytesIO(imageBytes))
    playersHand = list(data.get('playersHand'))
    sharedCards = list(data.get('sharedCards'))
    savedPlayersCards = data.get('savedPlayersCards')
    savedSharedCards = data.get('savedSharedCards')
    imageData = getImageData.getCardData(image)   
    if not savedPlayersCards and not savedSharedCards:
        sharedCards = []
        playersHand = []
        playersHand = imageData[:2]
        sharedCards = imageData[2:8]
    elif savedPlayersCards and not savedSharedCards:
        sharedCards = []
        for card in imageData:
            if card not in playersHand:
                sharedCards.append(card)
    elif not savedPlayersCards and savedSharedCards:
        playersHand = []
        for card in imageData:
            if card not in sharedCards:
                if len(playersHand) < 2:
                    playersHand.append(card)
                else:
                    sharedCards.append(card)

    handStrength = None
    potentialHands = []
    if len(playersHand) == 2:
        handStrength, potentialHands = handRankings.getHandRanking(playersHand, sharedCards)


    return jsonify({"handStrength": handStrength, "potentialHands": potentialHands, "playersHand": playersHand, "sharedCards": sharedCards}), 200


if __name__ == '__main__':
    app.run(debug=True)
