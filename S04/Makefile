PYTHON=python
SCRIPT=pbenc_chacha20_poly1305.py
KEY=chave.bin
MSG=mensagem.txt
ENC=$(MSG).enc
DEC=$(ENC).dec

all: setup enc dec

setup:
	$(PYTHON) $(SCRIPT) setup $(KEY)

enc:
	$(PYTHON) $(SCRIPT) enc $(MSG) $(KEY)

dec:
	$(PYTHON) $(SCRIPT) dec $(ENC) $(KEY)


clean:
	rm -f $(KEY) $(ENC) $(DEC)