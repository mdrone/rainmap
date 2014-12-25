RABBITMQLINK = http://www.rabbitmq.com/releases/rabbitmq-server/v3.4.2/rabbitmq-server-generic-unix-3.4.2.tar.gz
RABBITMQBASEDIR = rabbitmq
RABBITMQBIN = rabbitmq-server

all: install_rabbit start_rabbit

install_rabbit:
	mkdir -p $(RABBITMQBASEDIR)
	wget $(RABBITMQLINK)
	tar xvf $(notdir $(RABBITMQLINK)) -C $(RABBITMQBASEDIR) --strip-components=1
	rm $(notdir $(RABBITMQLINK))

start_rabbit:
	$(RABBITMQBASEDIR)/sbin/$(RABBITMQBIN) &

clean:
	echo rm -frv rabbitmq
