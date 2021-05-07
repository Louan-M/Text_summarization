import torch, gc
gc.collect()
torch.cuda.empty_cache()
import streamlit as st 
import smart_open
import time
import sumy
from rouge import Rouge
rouge = Rouge()
from summarizer import Summarizer
model = Summarizer()



# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

from transformers import pipeline
summarizer = pipeline("summarization")




import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm") 

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen



# Function for LexRank Summarization
def LexRank_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

def Lsa_summarizer(docx):
		parser = PlaintextParser.from_string(docx,Tokenizer("english"))
		lsa_summarizer = LsaSummarizer()
		summary_2 = lsa_summarizer(parser.document,3)
		summary_list_2 = [str(sentence) for sentence in summary_2]
		result_2 = ' '.join(summary_list_2)
		return result_2
	
def TextRank_summarizer(docx):
		parser = PlaintextParser.from_string(docx,Tokenizer("english"))
		text_rank_summarizer = TextRankSummarizer()
			
		summary_3 = text_rank_summarizer(parser.document,3)
		summary_list_3 = [str(sentence) for sentence in summary_3]
		result_3 = ' '.join(summary_list_3)
		return result_3

def Luhn_summarizer(docx):
		parser = PlaintextParser.from_string(docx,Tokenizer("english"))
		luhn_summarizer = LuhnSummarizer()
		summary_4 = luhn_summarizer(parser.document,3)
		summary_list_4 = [str(sentence) for sentence in summary_4]
		result_4 = ' '.join(summary_list_4)
		return result_4


# Fetch Text From Url
def get_text(url):
	
	from newspaper import fulltext
	import requests
	url = str(url)
	text = fulltext(requests.get(url).text)

	return text


def main():
	"""Summarizer Streamlit App"""

	st.title("Summarizer")

	activities = ["Summarize from Text","Summarize from URL", "Evaluation"]
	choice = st.sidebar.selectbox("Select Activity",activities)

	if choice == 'Summarize from Text':
		st.subheader("Summarize Document")
		raw_text = st.text_area("Enter Text Here","Type Here")
		summarizer_type = st.selectbox("Summarizer Type",["Lsa","Lex Rank", "Luhn", "Text Rank"])
		if st.button("Summarize"):
			import time
			start_time = time.monotonic()

			if summarizer_type == "Lex Rank":
				summary_result = LexRank_summarizer(raw_text)
				
			elif summarizer_type == "Luhn":
				summary_result = Luhn_summarizer(raw_text)

			elif summarizer_type == "Text Rank":
				summary_result = TextRank_summarizer(raw_text)
				
			else:
					summary_result = Lsa_summarizer(raw_text)

			st.write(summary_result)
			st.write('Execution time (seconds): ', time.monotonic() - start_time)

	if choice == 'Summarize from URL':
		st.subheader("Analysis on Text From URL")
		url = st.text_input("Enter URL Here","Type here")
		if st.button("Summarize"):
			if url != "Type here":
				result = get_text(url)
				len_of_text = len(result)
				st.success("Length of Full Text::{}".format(len_of_text))
				summarized_docx = LexRank_summarizer(result)
				st.write(summarized_docx)
	
	if choice == 'Evaluation':
		st.subheader("Comparison of summarization methods")	
		st.text("")
		st.write("Original article")
		st.text("")
		st.write('source: https://www.kaggle.com/sunnysai12345/news-summary/code')
		
		raw_text = "The Food Safety and Standards Authority of India (FSSAI) is in the process of creating a network of food bankingpartners to collect and distribute leftover food from large parties and weddings to the hungry.A notification to create a separate category of food business operators (FBOs), who will be licensed to deal only with leftover food, has been drafted to ensure the quality of food.?We are looking at partnering with NGOs or organisations that collect, store and distribute surplus food to ensure they maintain certain hygiene and health standards when handling food,? said Pawan Agarwal, CEO of FSSAI.?Tonnes of food is wasted annually. We are looking at creating a mechanism through which food can be collected from restaurants, weddings, large-scale parties,?  says Pawan Agarwal, ?All food, whether it is paid for or distributed free, must meet the country?s food safety and hygiene standards,? he said.The organisations in the business of collecting leftover food will now have to work in collaboration with FSSAI so their efforts can be scaled up.?Tonnes of food is wasted annually and can be used to feed several thousands. We are looking at creating a mechanism through which food can be collected from restaurants, weddings, large-scale parties etc,? said Agarwal.The initiative will set up a helpline network where organisations can call in for collection but reaching individuals who want to directly donate food will take time. ?We will have a central helpline number. Reaching people at the household level may not be feasible initially but it is an integral part of the long-term plan,? he said. ?We have begun collecting names of people working in the sector. There are still a few months to go before the scheme materialises,? said Agarwal.?Collecting food going waste to feed the hungry is a noble thought but to transport, store and maintain the cold chain of cooked food is a huge challenge. The logistics are a nightmare, which is why we don?t handle leftovers and only distribute uncooked food that can be cooked locally,? said Kuldip Nar, founder of Delhi NCR Food Bank, which has been feeding the poor in 10 cities since 2011."
		st.write(raw_text)
		length = len(raw_text)
		st.markdown('**Length of the document: **')
		st.write(length, "words")
		st.text("")
		st.text("")

		st.write("Reference summary")
		summary = "India's food regulator Food Safety and Standards Authority of India (FSSAI) is planning to create a network to collect leftover food and provide it to the needy. It is looking to connect with organisations which can collect, store and distribute leftover food from weddings and large parties. It further added that all food must meet the safety and hygiene standards."
		st.write(summary)
		length_summary = len(summary)
		st.markdown('**Length of the summary: **')
		st.write(length_summary, "words")
		st.text("")
		st.text("")
		
		
		if st.button("Compare methods"):


				import timeit
	

				Lsa = Lsa_summarizer(raw_text)

				st.text("")
				st.text("")


				start = timeit.default_timer()
				LexRank = LexRank_summarizer(raw_text)
				stop = timeit.default_timer()
				execution_time = stop - start

				st.write('LexRank:')
				st.write(LexRank)
				rouge_score = rouge.get_scores(LexRank, summary, avg=True)
				st.write('Rouge scores:')
				st.write(rouge_score)
				st.markdown('**Length of the summary: **')
				length_summary = len(LexRank)
				st.write(length_summary, "words")
				st.text("")
				st.write(f'Execution time: {execution_time} seconds' )
				st.text("")
				st.text("")



				start = timeit.default_timer()
				Luhn = Luhn_summarizer(raw_text)
				stop = timeit.default_timer()
				execution_time = stop - start

				st.text("")
				st.text("")
				st.write('Luhn:')
				st.write(Luhn)
				rouge_score = rouge.get_scores(Luhn, summary, avg=True)
				st.write('Rouge scores:')
				st.write(rouge_score)
				st.markdown('**Length of the summary: **')
				length_summary = len(Luhn)
				st.write(length_summary, "words")
				st.text("")
				st.write(f'Execution time: {execution_time} seconds' )
				st.text("")
				st.text("")



				start = timeit.default_timer()
				TextRank = TextRank_summarizer(raw_text)
				stop = timeit.default_timer()
				execution_time = stop - start
				
				st.text("")
				st.text("")
				st.write('TextRank:')
				st.write(TextRank)
				rouge_score = rouge.get_scores(TextRank, summary, avg=True)
				st.write('Rouge scores:')
				st.write(rouge_score)
				st.text("")
				st.text("")
				st.markdown('**Length of the summary: **')
				length_summary = len(TextRank)
				st.write(length_summary, "words")
				st.text("")
				st.write(f'Execution time: {execution_time} seconds' )
				st.text("")
				st.text("")


				start = timeit.default_timer()
				Lsa = Lsa_summarizer(raw_text)
				stop = timeit.default_timer()
				execution_time = stop - start


				st.write('Lsa:')
				st.write(Lsa)	
				rouge_score = rouge.get_scores(Lsa, summary, avg=True)
				st.write('Rouge scores:')
				st.write(rouge_score)
				st.text("")
				st.text("")
				st.markdown('**Length of the summary: **')
				length_summary = len(Lsa)
				st.write(length_summary, "words")
				st.text("")
				st.write(f'Execution time: {execution_time} seconds' )
				st.text("")
				st.text("")
				
				st.write('BertSum:')
				start = timeit.default_timer()

				result = model(raw_text, min_length=30,max_length=300)
				stop = timeit.default_timer()
				execution_time = stop - start
				summary_bert = "".join(result)
				st.write(summary_bert)
				st.text("")
				st.text("")
				rouge_score = rouge.get_scores(summary_bert, summary, avg=True)
				st.write('Rouge scores:')
				st.write(rouge_score)
				st.text("")
				st.text("")
				st.markdown('**Length of the summary: **')
				length_summary = len(summary_bert)
				st.write(length_summary, "words")
				st.text("")
				st.write(f'Execution time: {execution_time} seconds' )
				st.text("")
				st.text("")



				st.write('BART (Abstractive approach):')
				st.text("")
				st.text("")
				start = timeit.default_timer()
				result = summarizer(raw_text, do_sample=False)[0]['summary_text']
				stop = timeit.default_timer()
				execution_time = stop - start
				summary_bart = "".join(result)
				st.write(summary_bart)
				st.text("")
				st.text("")
				rouge_score = rouge.get_scores(summary_bart, summary, avg=True)
				st.write('Rouge scores:')
				st.write(rouge_score)
				st.text("")
				st.text("")
				st.markdown('**Length of the summary: **')
				length_summary = len(summary_bart)
				st.write(length_summary, "words")
				st.text("")
				st.write(f'Execution time: {execution_time} seconds' )
				st.text("")
				st.text("")




if __name__ == '__main__':
	main()

