struct Req{
1: string base64_img,
}

struct Response{
1: bool msg,
2: double occupation,
}

service OccupationService {
    Response predict(1:Req req);
}
