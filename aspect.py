import spacy
import en_core_web_md

aspects_found = []
aspect_found = ''
adjective_found = ''
aspect_found_flag = False
direct_aspect_found_flag = False 
adjective_found_flag = False
adjective_found_list = []
dobj_adjectives_found_list = []
negation_found_list = []

def get_determiner(token):
  determiner_aspect = ''
  if hasattr(token, 'children'):
    for child in token.children:
      if child.dep_ == "det" or child.pos_ == "DET":
        print("Determiner found." + " The determiner and nominal subject is: " + child.text + " " + token.text)
        determiner_aspect = child.text + " " + token.text
        return determiner_aspect
  else:
    return determiner_aspect

def get_dobj_amod(token):
  left_amod = ''
  right_amod = ''

  for left in token.lefts:
    if left.dep_ == 'amod' and left.pos_ == 'ADJ':
      dobj_adjectives_found_list.append(str(left.nbor(-1)) + left.text + str(left.nbor(1)))
      left_amod = " " + left.text + " "
      print("amod found " + left_amod)

  for right in token.rights:
    if right.dep_ == 'amod' and right.pos_ == 'ADJ':
      dobj_adjectives_found_list.append(right.nbor(-1).text + right.text + right.nbor(1).text)
      right_amod = " " + right.text
      print("amod found " + right_amod)
  
  if left_amod == '' and right_amod == '':
    return " " + token.text

  print("The amod is: " + left_amod + token.text + right_amod)
  return left_amod + token.text + right_amod

# gets adjective with any negations, adjective modifiers, or double adjectives
def get_adjective(token):
  # checks for negation
  negation = ''

  # checking for negation in ancestor tokens
  for ancestor in token.ancestors:
    if ancestor.dep_ == 'neg':
      negation_position = str(ancestor.nbor(-1) + child.text + str(ancestor.nbor(1)))
      if negation_position not in negation_found_list:
        negation_found_list.append(negation_position)
        negation = ancestor.text + " "
      continue

    for child in ancestor.children:
      if child.dep_ == 'neg':
        negation_position = child.nbor(-1).text + child.text + child.nbor(1).text
        if negation_position not in negation_found_list:
          negation_found_list.append(negation_position)
          negation = child.text + " "

          print("Negation found." + " The negation is: " + negation)

  # make this token.lefts??? and see if there is a difference 

  # checking for negation in child tokens
  for child in token.children:
      if child.dep_ == 'neg':
        negation = child.text + " "
      for c in child.children:
        if c.dep_ == 'neg':
          negation = child.text + " "
          print("Negation found." + " The negation is: " + negation)

  if negation == '':
    print("No negation was found")

  left_adjective = ''
  right_adjective = ''

 # checks for advmods of the adjective
  if len(list(token.lefts)) > 0:
    for left in token.lefts:
      if left.dep_ == 'advmod':
        print("Left advmod: " + left.text)
        left_adjective = left.text + " "
      if str(token.nbor(-1).pos_) == 'NOUN':
        left_adjective = token.nbor(-1).text + " "
              
  if len(list(token.rights)) > 0:
    for right in token.rights:
      if right.dep_ == 'advmod':
        print("right advmod: " + right.text)
        right_adjective = " " + right.text 
      if str(token.nbor(1).pos_) == 'NOUN':
        right_adjective = token.nbor(1).text + " "
  
  # constructing the final adjective 
  final_text = negation + left_adjective + token.text + right_adjective
  print("Final text is: " +  negation)

  return final_text
  
def get_dobj_verb(token):
  # checks for negation
  negation = ''

  # checking for negation in ancestor tokens
  for ancestor in token.ancestors:
    if ancestor.dep_ == 'dep':
      negation = ancestor.text + " "
      continue
    for child in ancestor.children:
      if child.dep_ == 'neg':
        negation = child.text + " "
        print("Negation found." + " The negation is: " + negation)
        # return negation

  # checking for negation in child tokens to the left 
  for child in token.lefts:
    if child.dep_ == 'neg':
      negation = child.text + " "
      print(negation)
    else:
      for c in child.children:
        if c.dep_ == 'neg' and c.pos_ == 'PART':
          negation = child.text + c.text + " "
          print("Negation found." + " The negation is: " + negation)

        if c.dep == 'neg':
          negation = child.text + " "
          print("Negation found." + " The negation is: " + negation)
          # return negation
            
  if negation == '':
    print("No negation was found")

  left_advmod = ''
  right_advmod = ''

   # checks for left advmods of the verb
  if len(list(token.lefts)) > 0:
    for left in token.lefts:
      if left.dep_ == 'advmod':
        print("Left advmod: " + left.text)
        left_advmod = left.text + " "
      elif left.dep_ == 'aux' and str(left.nbor(1).pos_) == 'PART':
        left_advmod = left.text + left.nbor(1).text + " "
      
  
  # checks for right advmods of the verb
  if len(list(token.rights)) > 0:
    for right in token.rights:
      if right.dep_ == 'advmod':
        print("right advmod: " + right.text)
        right_advmod = " " + right.text

  final_verb = negation + left_advmod + token.text + right_advmod
  return final_verb

# finds the noun nominal subject aspect
def Noun_nsubj(token):
  for ancestor in token.ancestors:
    if ancestor.pos_ == 'VERB':
      for child in ancestor.children:
        if child.dep_ == 'dobj':
          print("Direct object phrase found so will return")
          return

    # checking if a token has a determiner - eg. the, this, that
    global aspect_found
    aspect_found = get_determiner(token)

    # if no determiner was found then aspect is the current token
    if aspect_found == '' or aspect_found == None:
      print("No determiner for this aspect")
      aspect_found = token.text
    
    return aspect_found

# returns the pronoun or proper noun along with the nominal subject aspect if exists
def Pron_nsubj(token):
  for ancestor in token.ancestors:
    if ancestor.pos_ == 'VERB':
      for child in ancestor.children:
        if child.dep_ == 'dobj':
          print("Direct object phrase found so will return")
          return

    # checking if a token has a determiner - eg. the, this, that
    global aspect_found
    aspect_found = get_determiner(token)

    # if no determiner was found then aspect is the current token
    if aspect_found == '' or aspect_found == None:

      print("No determiner for this aspect") 
      aspect_found = token.text

    return aspect_found

# returns the determiner with a nominal subject aspect if exists
def Det_nsubj(token):
  for ancestor in token.ancestors:
    if ancestor.pos_ == 'VERB':
      for child in ancestor.children:
        if child.dep_ == 'dobj':
          print("Direct object phrase found so will return")
          return

    # checking if a token has a determiner - eg. the, this, that
    global aspect_found
    aspect_found = get_determiner(token.children)
  
    # if no determiner was found then aspect is the current token
  if aspect_found == '' or aspect_found == None:
    print("No determiner for this aspect")
    aspect_found = token.text
      
  return aspect_found

def main(tweetList):
  from collections import defaultdict
  final_aspects = []
  data_dict = defaultdict(list)
  nlp = spacy.load("en_core_web_md")
  for tweet in tweetList:
    doc = nlp(tweet)
    print("The tweet is: " + tweet)
    for sent in doc.sents:
      print("The sentence is: " + str(sent))
      for token in sent:
        # first condition finding nominal subject - aspect
        if token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
          aspect_found = Noun_nsubj(token)
          if aspect_found == '' or aspect_found is None:
            aspect_found = ''
            continue
          else:
            print("Aspect found is: " + aspect_found)
            global aspect_found_flag
            aspect_found_flag = True

        # finding nominal subject if it's a pronoun - aspect
        if token.pos_ == 'PRON' or token.pos_ == "PROPN" and token.dep_ == 'nsubj':
          aspect_found = Pron_nsubj(token)
          if aspect_found == '' or aspect_found is None:
            aspect_found = ''
            continue
          else:
            print("Aspect found is: " + aspect_found)
            aspect_found_flag = True

        # finding nominal subject if it's a determiner - aspect
        if token.pos_ == 'DET' and token.dep_ == 'nsubj':
          aspect_found = Det_nsubj(token)
          if aspect_found == '' or aspect_found is None:
            aspect_found = ''
            continue
          else:
            print("Aspect found is: " + aspect_found)
            aspect_found_flag = True
        
        # if token.pos_ == 'NOUN' and token.dep_ == 'pobj':
        #   aspect_found = Noun_nsubj(token)
        #   print("Aspect found is: " + aspect_found)
        #   if aspect_found == '' or aspect_found is None:
        #     continue
        #   else:
        #     aspect_found_flag = True
          

        # checks if verb is part of nominal and the direct subject
        if token.pos_ == 'VERB':
          nsubj = ''
          dobj = ''
          for left in token.lefts:
            print("The tokens in left are: " + left.text)
            if left.dep_ == 'nsubj':
              nsubj = left.text + " "
              print("The nsubj found is:" + nsubj)
          for right in token.rights:
            if right.dep_ == 'dobj':
              # gets amods on the left or right of the dobj token which is a Noun ???
              dobj = get_dobj_amod(right) 
              print("The dobj found is:" + dobj)

      # get the ordinary dobj aspect if dobj + verb exists otherwise find nsubj + verb + dobj else continue
          if nsubj != '' and dobj != '':
            verb_found = get_dobj_verb(token)
            print("Verb found is: " + verb_found)
            direct_aspect_found = nsubj + verb_found + dobj
            global direct_aspect_found_flag
            direct_aspect_found_flag = True
          elif nsubj == '' and dobj != '':
            verb_found = get_dobj_verb(token)
            print("Verb found is: " + verb_found)
            direct_aspect_found = nsubj + verb_found + dobj
            direct_aspect_found_flag = True
          else:
            continue

        # second condition finding adjective of aspect 
        if token.pos_ == 'ADJ':
          global adjective_found
          adjective_found = get_adjective(token)
          # can remove below line???
          if adjective_found != '':
            if adjective_found not in adjective_found_list:
              adjective_found_list.append(adjective_found)
              print("ADJ is: " + token.text)
              print("OK the ADJ is set here as: " + adjective_found)
              global adjective_found_flag
              adjective_found_flag = True
          
          # find length of sentence
          length = int(len(sent)) - 1

          if token.text == sent[length].text:
            print("Adj is the first token so can't look for right position so add '': " + token.text)
            adj_position = token.nbor(-1).text + token.text + ''
          elif token.text == sent[0].text:
            print("Adj is the first token so can't look for left position so add: '' " + token.text)
            adj_position = '' + token.text + token.nbor(1).text
          else:
            adj_position = token.nbor(-1).text + token.text + token.nbor(1).text
                  
          if adj_position in dobj_adjectives_found_list:
              adjective_found_flag = False
              continue

        global aspects_found
        if direct_aspect_found_flag == True:
          aspects_found.append("[The nominal subject and verb with direct object aspect is: " + direct_aspect_found + "]")
          direct_aspect_found_flag = False

        if aspect_found_flag == True and adjective_found_flag == True:
          aspects_found.append("[Aspect: " + aspect_found + " with an adjective of: " + adjective_found + "]")
          #print("The aspect flags are False")
          aspect_found_flag = False 
          adjective_found_flag = False

    final_aspects = aspects_found
    data_dict[tweet].append(final_aspects)
      
    # make sure all flags are set to false to avoid confilcts in next iteration
    aspect_found_flag = False
    direct_aspect_found_flag = False 
    adjective_found_flag = False
    aspects_found = []

    # if len(aspects_found) < 1:
    #   print("No aspect with an adjective was found.")
    #   print(aspects_found)

    # print(aspects_found)

  return data_dict

# if __name__ == '__main__':

#     tweet_list = ['I love food', 'I hate you']
#     data_dict = main(tweet_list)
#     for name in data_dict:
#       print("The tweet is: " + str(name) + " and aspects are: " + str(data_dict[name]))