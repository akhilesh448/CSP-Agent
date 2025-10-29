# ---- Build Stage ----
FROM golang:1.24-alpine AS builder

WORKDIR /app

COPY go_web_app/go.mod ./
RUN go mod download

COPY go_web_app/ .

RUN go build -o server main.go

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /app/server .

EXPOSE 8080

CMD ["./server"]
