def chunker(pages):
    chunks =[]
    chunk_count=0
    
    
    new_length=0
    overlap=30
    for i,page in enumerate(pages):
        start = 0
        reduced_length = len(page['text'])//3
       
        dictionary = {"page_number": None, "chunk_id": None, "text": None}
        for i in range(4):
            dictionary['page_number']= page['page_number']
            if(i>0):
                new_length = reduced_length+new_length-overlap
            else:
                new_length = reduced_length+new_length

            dictionary["chunk_id"]= chunk_count
            dictionary["text"]=page["text"][start:new_length]
            start = start +reduced_length-overlap
            
            
            chunk_count +=1
            chunks.append(dictionary)
            dictionary = {"page_number": None,"chunk_id":None,"text":None}
        new_length=0

        
    return chunks