.PHONY : main

MAIN=paper
LATEX=pdflatex

all: paper tidy

paper: $(MAIN).tex
	$(LATEX) $(MAIN)
	bibtex $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

tidy:
	rm -f *.dvi *.aux *.log *.nav *.snm *.toc *.out *.vrb *.bbl *.blg

clean:
	rm -f *.dvi *.aux *.log *.nav *.snm *.toc *.out *.vrb *.bbl *.blg $(MAIN).ps $(MAIN).pdf
