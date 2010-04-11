APP=gmilk
BIN=/usr/bin/gmilk
BASE=/usr/local/share/$(APP)
LIB=$(BASE)/lib/
IMAGES=$(BASE)/images/
LOCALE=/usr/share
MO_INSTALL=$(shell find -iname '*.mo' -exec sh -c "dirname {} | cut -b2-" \;)
MO_REMOVE=$(shell find $(LOCALE)/locale/ -iname '$(APP).mo')

install:
	mkdir -p $(LIB)
	mkdir -p $(IMAGES)
	cp *.py $(LIB)
	rm -f $(BIN)
	ln -s $(LIB)/gmilk.py $(BIN) 
	cp images/* $(IMAGES)
	@for TRANSLATION in $(MO_INSTALL); do \
		echo "Installing $${TRANSLATION}"; \
		cp .$${TRANSLATION}/$(APP).mo $(LOCALE)$${TRANSLATION}/$(APP).mo; \
	done

uninstall:
	rm -f $(BIN)
	rm -f $(LIB)/*
	rm -f $(IMAGES)/*
	rmdir $(LIB)
	rmdir $(IMAGES)
	rmdir $(BASE)
	@for TRANSLATION in $(MO_REMOVE); do \
		echo "Removing $${TRANSLATION}"; \
		rm $${TRANSLATION}; \
	done
