# authserver

기존 데이터베이스를 활용한 JWT 발급/인증 서버입니다.

- MSA 환경을 구축하기 위한 필수 서버로 아직 서비스가 작을 때 미리 인증 서버와 그 외 서버를 분리하는 작업입니다.
- 기존 pampam_api에서 JWT를 발급하는 모든 로직을 사용하기 때문에 (시그니처 키, 알고리즘, 데이터를 담는 범위) 인증서버에서 발급한 토큰이 현재 배포되어있는 서버와 연동이 쉽게 가능할 것이라 예상

기존 JWT 인증 로직

```python
@router.post("/login/access-token", response_model=Optional[schemas.User], summary="일반_유저_이메일_비밀번호_로그인")
def get_user_detail_with_tokens_by_email_and_password(
    email: EmailStr,
    password: str,
    db: Session = Depends(deps.get_db),
    ) -> Any:
    """
    사용자 이메일 비밀번호 인증 후 토큰 반환
    """
    error = ErrorBuilder().user().login().add_input(f"{crud.inspect.stack()[0][3]} :: email: {email}, password: {password}")
    user = crud.user.get_by_email_general(db=db, email=email)
    if user:
        if crud.user.is_banned(user):
            raise HTTPException(HTTP_400_BAD_REQUEST, ErrorBuilder().error_log(192, "보호조치된 계정입니다."))
        if not crud.user.is_active(user):
            raise HTTPException(HTTP_400_BAD_REQUEST, ErrorBuilder().error_log(191, "탈퇴 회원입니다. 탈퇴 후 7일동안 다시 가입할수 없어요."))
    user = crud.user.authenticate(db, email=email, password=password)
    if not user:
        raise HTTPException(HTTP_400_BAD_REQUEST, ErrorBuilder().error_log(192, "이메일 또는 패스워드가 올바르지 않습니다. 다시 입력해주세요."))
    user.token = security.get_all_new_tokens(id=user.id)
    return user
```

바뀐 로그인 로직

```python
@router.post('/token/pair', response={200: Token, 401: Error})
def token_obtain_pair(request, auth: AuthSchema):
    """사용자의 email과 password를 입력받아 JWT를 발급합니다.

    Args:
        auth (AuthSchema): {email: str, password: str}
    """
    user_filter = User.objects.filter(email=auth.email)

    if user_filter.exists():
        user = user_filter.first()
        if Hasher.check_user_is_allowed(auth.password, user):
            return 200, JWTMiddleware.get_all_new_tokens(user.id)

    return 401, {
        'code': 401,
        'message': '올바르지 않은 계정입니다.'
    }
```

### 인증 서버 고려사항

- 모든 에러 코드(status code)는 표준 코드를 사용

  - 현재 로그를 작성하는 클래스 ErrorBuild에는 다양한 상태코드가 존재함

  ```python
  ...
  def user(self):                                     self.add(code= 100, message="사용자");                                  return self
  def item(self):                                     self.add(code= 200, message="상품");                                    return self
  def address(self):                                  self.add(code= 300, message="주소");                                    return self
  def deal(self):                                     self.add(code= 400, message="채팅");                                    return self
  def review(self):                                   self.add(code= 500, message="후기");                                    return self
  def device(self):                                   self.add(code= 600, message="기기");                                    return self
  def contact_request(self):                          self.add(code= 700, message="거래 제안");                               return self
  def trade_request(self):                            self.add(code= 800, message="거래 처리");                               return self
  def management(self):                               self.add(code= 900, message="관리");                                    return self
  def service_notice(self):                           self.add(code=1000, message="공지사항");                                return self
  def service_faq(self):                              self.add(code=1100, message="자주묻는 질문");                           return self
  def service_qna(self):                              self.add(code=1200, message="1대1 문의하기");                           return self
  def report(self):                                   self.add(code=1300, message="신고");                                    return self
  def bank_account(self):                             self.add(code=1400, message="인출계좌");                                return self
  def cashout_request(self):                          self.add(code=1500, message="인출요청");                                return self
  def charge_request(self):                           self.add(code=1600, message="입금확인 요청");                           return self
  def token(self):                                    self.add(code=1700, message="토큰");                                    return self
  def transaction(self):                              self.add(code=1800, message="트랜잭션");                                return self
  def point(self):                                    self.add(code=1900, message="포인트");                                  return self
  def comment(self):                                  self.add(code=2000, message="댓글");                                    return self
  def shopping_history(self):                         self.add(code=2100, message="거래내역");                               return self
  def unknown_22(self):                               self.add(code=2200, message="미확인_22");                               return self
  def unknown_23(self):                               self.add(code=2300, message="미확인_23");                               return self
  def unknown_24(self):                               self.add(code=2400, message="미확인_24");                               return self
  ...
  ```

  - 모든 상태 코드를 표준 상태 코드로 변경하고 구분은 API endpoint로 통일
    1. 상태코드가 여러개일 수록 나중에 로그를 분석하는 파이프라인이나 툴을 사용한다거나 개발할 때 개발 시간, 유지보수의 어려움이 예상됨.
    2. 표준 상태코드와 엔드포인트로 구분한다면 이와 같은 문제를 해결할 수 있을 것이라 생각됨.
    3. 표준 상태코드로 표현할 수 없는 매우 특수한 상황에서는 600코드로 통일

### 진행상황

1. 현재 사용하는 데이터베이스와 연동하여 기존의 유저 데이터로 JWT발급 성공
2. 토큰 발급, 리프레시, 인증 로직 구현

### 진행예정

1. 소셜 로그인 연동
2. 로그 작성 로직 구현
3. 발급 받은 토큰으로 현재 구현되어있는 pampam_api의 모든 api endpoint 테스트
4. 유저의 상태에 따른 여러 메세지 출력

```python
...
if user:
        if crud.user.is_banned(user):
            raise HTTPException(HTTP_400_BAD_REQUEST, ErrorBuilder().error_log(192, "보호조치된 계정입니다."))
        if not crud.user.is_active(user):
            raise HTTPException(HTTP_400_BAD_REQUEST, ErrorBuilder().error_log(191, "탈퇴 회원입니다. 탈퇴 후 7일동안 다시 가입할수 없어요."))
...
```

    - 아직 여러 상태에 따라 다른 메세지를 출력하지는 않음.
