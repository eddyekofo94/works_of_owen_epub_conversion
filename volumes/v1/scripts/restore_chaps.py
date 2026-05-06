import re
import os

def restore():
    with open('books/Owen/volumes/v1/intermediate/volume_1.thml.xml', 'r') as f:
        content = f.read()

    ch9_text = """    <div1 title="CHAPTER 9" id="ch018">
      <h2>CHAPTER 9</h2>
      <p class="Body">
        <b>HONOR DUE TO THE PERSON OF CHRIST — THE NATURE </b>
        <b>AND CAUSES OF IT </b>
      </p>
      <p class="Body">Many other considerations of the same nature with those foregoing, relating unto the glory and honor of the person of Christ, may be taken from all the fundamental principles of religion. And our duty it is in them all, to “consider the Apostle and High Priest of our profession” — “the Author and Finisher of our faith”. I shall not insist on more, but proceed unto those principles of truth which are immediately directive of our duty towards him; without diligent attendance whereunto, we do but in vain bear the name of Christians. And the substance of what is designed may be included in the following assertion: — </p>
      <p class="Body">“The glory, life, and power of Christian religion, as Christian religion, and as seated in the souls of men, with all the acts and duties which properly belong thereunto, and are, therefore, peculiarly Christian, and all the benefits and privileges we receive by it, or by virtue of it, with the whole of the honor and glory that arise unto God thereby, have all of them their formal nature and reason from their respect and relation unto the person of Christ; nor is he a Christian who is otherwise minded.” </p>
      <p class="Body">In the confirmation hereof it will appear what judgment ought to be passed on that inquiry — which, after the uninterrupted profession of the catholic church for so many ages of a faith unto the contrary, is begun to be made by some amongst us — namely, Of what use is the person of Christ in religion? For it proceeds on this supposition, and is determined accordingly — that there is something in religion wherein the person of Christ is of no use at all; — a vain imagination, and such as is destructive unto the whole real intercourse between God and man, by the one and only Mediator! The respect which we have in all acts of religion unto the person of Christ may be reduced unto these four heads: </p>
    </div1>\n"""

    ch18_text = """    <div1 title="CHAPTER 18" id="ch032">
      <h2>CHAPTER 18</h2>
      <p class="Body">
        <b>THE NATURE OF THE PERSON OF CHRIST, AND THE </b>
        <b>HYPOSTATICAL UNION OF HIS NATURES DECLARED </b>
      </p>
      <p class="Body">The nature or constitution of the person of Christ hath been commonly spoken unto and treated of in the writings both of the ancient and modern divines. It is not my purpose, in this discourse, to handle anything that hath been so fully already declared by others. Howbeit, to speak something of it in this place is necessary unto the present work; and I shall do it in answer unto a double end or design: — First, To help those that believe, in the regulation of their thoughts about this divine person, so far as the Scripture goes before us. It is of great importance unto our souls that we have right conceptions concerning him; not only in general, and in opposition unto the pernicious heresies of them by whom his divine person or either of his natures is denied, but also in those especial instances wherein it is the most ineffable effect of divine wisdom and grace. For although the knowledge of him mentioned in the Gospel be not confined merely unto his person in the constitution thereof, but extends itself unto the whole work of his mediation, with the design of God’s love and grace therein, with our own duty thereon; yet is this knowledge of his person the foundation of all the rest, wherein if we mistake or fail, our whole building in the other parts of the knowledge of him will fall unto the ground. And although the saving knowledge of him is not to be obtained without especial divine revelation, Matthew 16:17 — or saving illumination, 1 John 5:20 — nor can we know him perfectly until we come where he is to behold his glory, John 17:. 24; yet are instructions from the Scripture of use to lead us into those farther degrees of the knowledge of him which are attainable in this life. Secondly, To manifest in particular how ineffably distinct the relation between the Son of God and the man Christ Jesus is, from all that relation and union which may be between God and believers, or between God and any other creature. The want of a true understanding hereof is the fundamental error of many in our days. We shall manifest thereupon how “it pleased the Father that in him should all fullness dwell,” so that in all things “he might have the pre- eminence,” Colossians 1:18, 19. And I shall herein wholly avoid the  curious inquiries, bold conjectures, and unwarrantable determinations of the schoolmen and some others. For many of them, designing to explicate this mystery, by exceeding the bounds of Scripture light and sacred sobriety, have obscured it. Endeavoring to render all things plain unto reason, they have expressed many things unsound as unto faith, and fallen into manifold contradictions among themselves. Hence Aquinas affirms, that three of the ways of declaring the hypostatical union which are proposed by the Master of the Sentences, are so far from probable opinions, as that they are downright heresies. I shall therefore confine myself, in the explication of this mystery, unto the propositions of divine revelation, with the just and necessary expositions of them. What the Scripture represents of the wisdom of God in this great work may be reduced unto these four heads: — </p>
    </div1>\n"""

    # Check if ch020 exists and ch018 doesn't
    if 'id="ch018"' not in content:
        m = re.search(r'<div1[^>]*id="ch020"[^>]*>', content)
        if m:
            content = content[:m.start()] + ch9_text + content[m.start():]
            print("Restored ch018")
        else:
            print("ch020 missing")
    else:
        print("ch018 already exists")

    # Check if ch034 exists and ch032 doesn't
    if 'id="ch032"' not in content:
        m = re.search(r'<div1[^>]*id="ch034"[^>]*>', content)
        if m:
            content = content[:m.start()] + ch18_text + content[m.start():]
            print("Restored ch032")
        else:
            print("ch034 missing")
    else:
        print("ch032 already exists")

    with open('books/Owen/volumes/v1/intermediate/volume_1.thml.xml', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    restore()
