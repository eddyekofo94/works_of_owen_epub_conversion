from extract import post_process_paragraphs

paragraphs = [
    '**3dly**. The intercession of the saints thus assisted is according to the mind of God; that is, they are guided by the Spirit to make requests for those things unto God which it is his will they should desire, — which he knows to be good for them, useful and suitable to them, in the condition wherein they are. There are many ways whereby we may know when we make our supplications according to the will of God. I shall instance only in one; that is, when we do it according to the promise: when our prayers are regulated by the promise, we make them according to the will of God. So David, Psalm 119:49, "Remember the word upon which thou hast caused me to hope." He prays, and regulates his desire by the word of promise wherein he had trusted. But yet, men may ask that which is in the promise, and yet not have their prayers regulated by the promise. They may pray for what is in the promise, but not as it is in the promise. So James says some "ask and receive not, because they ask amiss, that they may spend it on their lusts," chap. 4:3. Though the things which God would have us ask be requested, yet if not according as he would have us do it, we ask amiss.',
    'Two things are required, that we may pray for the things in the promise, as they are in the promise: — (1st.) That we look upon them as promised, and promised in Christ; that is, that all the reason we have whence we hope for attaining the things we ask for, is from the mediation and purchase of Christ, in whom all the promises are yea and amen. This it is to ask the Father in Christ\'s name, — God as a father, the fountain; and Christ as the procurer of them.',
    '(2ndly.) That we ask for them for the end of the promise, not to spend on our lusts. When we ask pardon for sin, with secret reserves in our hearts to continue in sin, we ask the choicest mercy of the covenant, to spend it on our lusts. The end of the promise the apostle tells us, 2 Corinthians 7:1,'
]

cleaned = post_process_paragraphs(paragraphs)
for i, p in enumerate(cleaned):
    print(f"P{i}: [{p}]")
