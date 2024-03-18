FROM python:3.11

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /tmp

RUN wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz \
    && tar -xf install-tl-unx.tar.gz \
    && rm install-tl-unx.tar.gz \
    && cd install-tl-* \
    && echo "selected_scheme scheme-basic" > profile.txt \
    && ./install-tl --profile=profile.txt \
    && cd .. \
    && rm -rf install-tl-*

ENV PATH="/usr/local/texlive/2024/bin/x86_64-linux:${PATH}"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY create_pdf.py .

RUN mkdir artifacts data

CMD ["python", "create_pdf.py"]