# text-image-nft
Text->Image->NFT generation app

Firstly, we generate an image(s) from the provided text description using two models:
1. Stable Diffusion free model through diffusers.StableDiffusionPipeline;
2. OpenAI API model through;

Secondly, we can save the generated image and upload it as NFT to OpenSea using:
1. selenium.webdriver to link MetaMask, upload to OpenSea;
2. Lazy Mint - minting at the moment of purchase - for NFT creation;
