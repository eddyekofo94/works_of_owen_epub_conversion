We have a critical semantic disintegration issue where the layout parser atomizes unified paragraphs into fragmented, single-sentence blocks (for example, on Volume 2, Print Page 343). Because every broken block contains grammatically valid words, our standard validation tests completely miss it.
To catch and prevent this across all 16 volumes, we need to establish a Hard Integrity Budget for Layout Fragmentation directly within our build pipeline. Please implement the following architecture changes across shared.py, converter.py, and our text-integrity audit scripts:
1. Add Text-Density Constants to shared.py
Add structural budget limits to our configuration to catch layout disintegration:
# Text-Integrity Threshold Budgets
MIN_WORD_COUNT_PER_PARAGRAPH = 35.0  # Puritan prose rarely averages less than this per chapter
MAX_MALFORMED_TRANSITION_RATE = 0.08  # Max 8% of paragraphs allowed to break mid-clause

2. Implement the Integrity Budget Check
Add this verification step to the automated build gate. If a chapter blows its paragraph distribution budget or exhibits systemic layout line-splitting, it must trip a hard failure and halt the build.
import re

def verify_paragraph_integrity_budget(text_blocks, volume_num, chapter_id):
    """
    Enforces a strict statistical integrity budget against aggressive paragraph 
    fragmentation caused by raw PDF layout extraction.
    """
    # Exclude small metadata sections like front matter/TOC
    if len(text_blocks) < 5:
        return True

    total_paragraphs = len(text_blocks)
    total_words = sum(len(p.split()) for p in text_blocks)
    avg_words_per_p = total_words / total_paragraphs
    
    malformed_transitions = 0
    
    for i in range(len(text_blocks) - 1):
        p1 = text_blocks[i].strip()
        p2 = text_blocks[i+1].strip()
        
        if not p1 or not p2:
            continue
            
        # Rule A: Paragraph ends on a non-terminal punctuation mark or dangling connector
        if p1[-1] in [',', ';', ':', '—'] or p1.split()[-1].lower() in ['and', 'the', 'of', 'to', 'that', 'with']:
            malformed_transitions += 1
            
        # Rule B: Next paragraph begins with a lowercase letter while previous lacked a terminal mark
        elif p2[0].islower() and p1[-1] not in ['.', '!', '?', '"', '”']:
            malformed_transitions += 1

    transition_rate = malformed_transitions / total_paragraphs if total_paragraphs > 0 else 0

    if avg_words_per_p < MIN_WORD_COUNT_PER_PARAGRAPH:
        raise ValueError(
            f"[CRITICAL PARAGRAPH BREAK FAILURE] Vol {volume_num} {chapter_id} blew its integrity budget!\n"
            f"Average words per paragraph is {avg_words_per_p:.2f} (Minimum threshold: {MIN_WORD_COUNT_PER_PARAGRAPH}).\n"
            f"Prose is severely fragmented."
        )
        
    if transition_rate > MAX_MALFORMED_TRANSITION_RATE:
        raise ValueError(
            f"[CRITICAL TRANSITION FAILURE] Vol {volume_num} {chapter_id} exceeds broken sentence transitions!\n"
            f"Transition Failure Rate: {transition_rate:.2%}. The layout engine is injecting artificial breaks."
        )

    return True

3. Refine the Extraction Preprocessor in converter.py
Before generating structural paragraphs, let's fix the layout artifact directly at the boundary level. Update the extraction block logic to look for consecutive text blocks where the preceding line doesn't terminate a logical sentence:
def heal_extracted_layout_fragments(text_blocks):
    """
    Heals artificial layout breaks before writing to final XHTML structures.
    """
    healed_blocks = []
    current_block = ""

    for block in text_blocks:
        block = block.strip()
        if not block:
            continue

        if current_block:
            # Check if current_block ends mid-sentence or mid-clause
            ends_infelicitously = current_block[-1] in [',', ';', ':', '—'] or current_block.split()[-1].lower() in ['and', 'the', 'of', 'to', 'that', 'with']
            ends_without_terminal = current_block[-1] not in ['.', '!', '?', '"', '”']
            starts_with_lowercase = block[0].islower()

            if ends_infelicitously or (ends_without_terminal and starts_with_lowercase):
                # Heal the split by joining the blocks with a single space
                current_block = f"{current_block} {block}"
                continue
            else:
                healed_blocks.append(current_block)
                current_block = block
        else:
            current_block = block

    if current_block:
        healed_blocks.append(current_block)

    return healed_blocks

Please run a regeneration of Volume 2 once these constraints are introduced. The automated validation gate must successfully capture the structural errors on page 343 before the healing preprocessor remedies it.
