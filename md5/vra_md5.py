import hashlib


def md5_crack(hexhash, template, wildcard, symbolranges):
    # first block recursively instantiates template
    # print("/vra_md5_crack: Template to try: " + template)
    i = 0
    found = False
    for symbolrange in symbolranges:
        start_symbol = symbolrange[0]
        end_symbol = symbolrange[1]
        while i < len(template):
            if template[i] == wildcard:
                found = True
                char = start_symbol  # start with this char ascii
                while char < end_symbol:
                    c = chr(char)
                    if c != wildcard:  # cannot check wildcard!
                        ntemplate = template[:i] + c + template[i + 1:]
                        # print("i: "+str(i)+" ntemplate: "+ntemplate)
                        res = md5_crack(hexhash, ntemplate, wildcard, symbolranges)
                        if res:  # stop immediately if cracked
                            return res
                    char += 1
            i += 1
    # instantiation loop done
    if not found:
        # no wildcards found in template: crack
        m = hashlib.md5()
        m.update(template)
        hash = m.hexdigest()
        # print("template: "+template+" hash: "+hash)
        if hash == hexhash:
            return template  # cracked!
    # template contains wildcards
    return None
