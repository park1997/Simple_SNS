import time
import pandas as pd
from bs4 import BeautifulSoup
import lxml
import requests
import numpy as np


class DonggukTime:
    """
    DonggukTime class(For Engineers)
    Author : Park ByeongHyeon
    Date : 2020-11-23
    """
    #클래스 인스턴스 순서 저장 하기위해
    user_index=0
    #가입된 회원의 정보들(이름과 아이디)
    member_in_this_system=[]
    #df전역변수로 설정(타임라인)
    df_timeline=pd.read_excel("timeline.xlsx")
    #df전역변수로 설정(아이디,패스워드)
    df_idpw=pd.read_excel("ID,PW.xlsx")
    #__init__
    def __init__(self,details):
        self.name=details[0]
        self.id=details[1]
        self.pw=details[2]
        self.birth=details[3]
        print(self.name, self.id, self.pw,self.birth)
    #타임라인 보여주기
    def show_timeline(self):
        df_timeline_sorted=DonggukTime.df_timeline.sort_values(["작성시간"],ascending=False)
        if len(df_timeline_sorted)==0:
            print("현재 타임라인에 글이 없습니다.")
        for i in range(len(df_timeline_sorted)):
            name,time,context,likes_num,grade,lecture_name,head_name,comment,id_timeline,professor_name,like_id=df_timeline_sorted.iloc[i]
            print("{} 번째 강의 평 : {}".format(len(df_timeline_sorted)-i,head_name))
            print("{}".format("-"*50))
            print("좋아요 : {}".format(likes_num))
            print("{}".format("-"*50))
            print("작성자 : {}\tID : {}\n작성 시간: {}".format(name,id_timeline,time))
            print("{}".format("-"*50))
            print("과목 명 : {}\t교수님 성함 : {}\n강의 평점 : {}".format(lecture_name,professor_name,grade))
            print("{}".format("-"*50))
            print("강의 평 내용\n")
            print(context)
            print("{}".format("="*50))
            print("댓글\n")
            print("{}".format(comment))
            print()
            print()
    #타임라인 작성하기
    def write_timeline(self):
        post_head_name=input("글 제목을 입력 하세요.  >>")
        post_context=input("글 내용을 입력 하세요.  >>")
        post_lecture=input("강의 이름을 입력 하세요.  >>")
        #실수로 띄어쓰기로 강의명을 입력했을경우 공백을 제거해준다.
        post_lecture="".join(post_lecture)
        post_professor_name=input("교수님의 성함을 입력 하세요. >>")
        #실수로 띄어쓰기로 교수명을 입력했을경우 공백을 제거해준다.
        post_professor_name="".join(post_professor_name)
        while 1:
            try:
                post_grade=float(input("강의 평점을 0점 이상 10점 이하로 입력해 주세요. >>"))
                if post_grade>10:
                    print("점수 범위를 초과 하셨습니다. 10점 이하로 입력해 주세요.  >>")
                elif post_grade<0:
                    print("점수를 양수로 입력해 주세요.  >>")
                else:
                    break
            except :
                #강의 평점을 문자로 입력한경우!
                print("숫자로 입력해 주세요!")
        now=time.localtime()
        post_now_time="%04d/%02d/%02d %02d:%02d:%02d"%(now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)

        print("성공적으로 글을 포스팅 하셨습니다. ")
        print()
        DonggukTime.df_timeline=DonggukTime.df_timeline.append({"작성자":self.name,"작성시간":post_now_time,"글내용":post_context,"좋아요수":0,"평점":post_grade,"과목명":post_lecture,"글제목":post_head_name,"댓글":"","아이디":self.id,"교수님성함":post_professor_name,"좋아요아이디":0},ignore_index=True)
        #바뀐 DataFrame을 excel에 저장
        DonggukTime.df_timeline.to_excel("timeline.xlsx",index=False)
    #내가 쓴 글 삭제하기
    def delete_post(self):
        #작성자가 현재 객체의 아이디와 같은경우(아이디는 중복으로 생성 못하게 했으므로.)
        for_delete_dic={}
        for i,j in enumerate(DonggukTime.df_timeline["아이디"]):
            if j==user.id:
                for_delete_dic[i]=[DonggukTime.df_timeline["글제목"].iloc[i],DonggukTime.df_timeline["글내용"].iloc[i],DonggukTime.df_timeline["아이디"].iloc[i]]
                print("{} - {}".format(i,DonggukTime.df_timeline["글제목"][i]))
        post_num=int(input("삭제할 본인의 게시물 번호를 입력해 주세요.  >>"))
        #DataFrame에 삭제할 index 계산(글제목과 내용이 같은 사람이 썼을 경우,본인이 썼을 경우)
        for i in range(len(DonggukTime.df_timeline)):
            if (DonggukTime.df_timeline["작성자"][i]==self.name) and (DonggukTime.df_timeline["글제목"].iloc[i]==for_delete_dic[post_num][0]) and (DonggukTime.df_timeline["글내용"].iloc[i]==for_delete_dic[post_num][1]) and (DonggukTime.df_timeline["아이디"].iloc[i]==for_delete_dic[post_num][2]):
                index_num_delete=i
                break
        #DataFrame에 해당 행 삭제
        DonggukTime.df_timeline.drop(DonggukTime.df_timeline.index[index_num_delete],inplace=True)
        #실제엑셀파일에 저장
        DonggukTime.df_timeline.to_excel("timeline.xlsx",index=False)

        print("정상적으로 삭제 되었습니다.")
    #선이수 관계 보여주기
    def standing_mc_the_max(self):
        #모든 엑셀 파일들의 데이터를 불러온다.
        ise_df = pd.read_excel("산시선이수.xlsx")
        cee_df = pd.read_excel("건설환경공학선이수.xlsx")
        mre_df = pd.read_excel("기계공학선이수.xlsx")
        mme_df = pd.read_excel("멀티미디어선이수.xlsx")
        ice_df = pd.read_excel("정보통신공학선이수.xlsx")
        cse_df = pd.read_excel("컴퓨터공학선이수.xlsx")
        cbe_df = pd.read_excel("화생공선이수.xlsx")
        eee_df = pd.read_excel("전자전기공학선이수.xlsx")
        gunchuk_df = pd.read_excel("건축공학선이수.xlsx")
        architec_df = pd.read_excel("건축학선이수.xlsx")
        newmeterial_df = pd.read_excel("융에신선이수.xlsx")
        #불러온 데이터를 모두 이 딕셔너리에 넣는다
        df_dic={}
        k=0
        for i in ise_df['후수교과목']:
            df_dic[i]=ise_df['선수교과목'][k]
            k+=1
        k=0
        for i in cee_df['후수교과목']:
            df_dic[i]=cee_df['선수교과목'][k]
            k+=1
        k=0
        for i in mre_df['후수교과목']:
            df_dic[i]=mre_df['선수교과목'][k]
            k+=1
        k=0
        for i in mme_df['후수교과목']:
            df_dic[i]=mme_df['선수교과목'][k]
            k+=1
        k=0
        for i in ice_df['후수교과목']:
            df_dic[i]=ice_df['선수교과목'][k]
            k+=1
        k=0
        for i in cse_df['후수교과목']:
            df_dic[i]=cse_df['선수교과목'][k]
            k+=1
        k=0
        for i in cbe_df['후수교과목']:
            df_dic[i]=cbe_df['선수교과목'][k]
            k+=1
        k=0
        for i in eee_df['후수교과목']:
            df_dic[i]=eee_df['선수교과목'][k]
            k+=1
        k=0
        for i in gunchuk_df['후수교과목']:
            df_dic[i]=gunchuk_df['선수교과목'][k]
            k+=1
        k=0
        for i in architec_df['후수교과목']:
            df_dic[i]=architec_df['선수교과목'][k]
            k+=1
        k=0
        for i in newmeterial_df['후수교과목']:
            df_dic[i]=newmeterial_df['선수교과목'][k]
            k+=1
        lec_name=input(" 과목명을 입력 하세요.  >>")
        #혹시 사용자 실수로 띄어쓰기 했을경우 고려.
        lec_name=''.join(lec_name.split())
        if lec_name in df_dic:
            result=df_dic[lec_name]
            print("\"{}\"의 선 이수 과목은 \"{}\" 입니다. ".format(lec_name,result))
        else:
            print("\"{}\"은 선이수 과목이 없습니다. ".format(lec_name))
    #PW변경
    def edit_profile_pw(self):
        while 1:
            first_pw_input=input("변경할 Password를 입력해 주세요. >>")
            second_pw_input=input("Password를 다시 한번 입력해 주세요. >>")
            print()
            if first_pw_input==second_pw_input:
                break
            else:
                print("Password가 일치 하지 않습니다. 변경할 Password를 다시 입력해 주세요.")
                print()
        delete_index=""
        for i,j in enumerate(DonggukTime.df_idpw["아이디"]):
            if self.id==j:
                delete_index=i
                break
        DonggukTime.df_idpw.loc[delete_index,"패스워드"]="String"
        DonggukTime.df_idpw.loc[delete_index,"패스워드"]=first_pw_input
        DonggukTime.df_idpw.to_excel("ID,PW.xlsx",index=False)
        user=DonggukTime([DonggukTime.df_idpw["이름"][user_index],DonggukTime.df_idpw["아이디"][user_index],DonggukTime.df_idpw["패스워드"][user_index],DonggukTime.df_idpw["생년월일"][user_index]])
        print("Password 변경에 성공 하셨습니다.\n")
    #댓글 작성
    def write_comment(self):
        for i,j in enumerate(DonggukTime.df_timeline["글제목"]):
            print("{} - {}".format(i,j))
        post_num=int(input("댓글을 달 게시물의 번호를 입력해 주세요.  >>"))
        post_comment=input("댓글을 입력해 주세요. >>")
        #판다스의 경고문을 무시함
        pd.options.mode.chained_assignment = None
        #댓글추가
        temp=DonggukTime.df_timeline["댓글"][post_num]
        now=time.localtime()
        commenttime_now_time="%04d/%02d/%02d %02d:%02d:%02d"%(now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
        temp1="{} : {}\t\t{}".format(self.name,post_comment,commenttime_now_time)
        temp2=str(temp)+"\n"+str(temp1)
        #초기화후 댓글 추가
        DonggukTime.df_timeline.loc[post_num,"댓글"]="String"
        DonggukTime.df_timeline.loc[post_num,"댓글"]=temp2
        #Unnamed열 생성 억제
        DonggukTime.df_timeline.to_excel("timeline.xlsx",index=False)
        print("댓글 입력 완료!")
    #좋아요 누르기
    def like(self):
        #한 게시물에 한아이디로 하나의 좋아요만 누를수 있게하기위해
        like_dic={}
        for i,j in enumerate(DonggukTime.df_timeline["글제목"]):
            like_dic[j]=[]
            print("{} - {}".format(i,j))
        print()
        like_num=int(input("좋아요를 누를 게시물의 번호를 입력하세요. >>"))
        print()
        #판다스의 경고문을 무시함
        pd.options.mode.chained_assignment = None
        temp=DonggukTime.df_timeline["좋아요아이디"].iloc[like_num]
        if str(temp) == str(0) :   #비어있는 셀
            #판다스의 경고문을 무시함
            pd.options.mode.chained_assignment = None
            temp=self.id
            DonggukTime.df_timeline.loc[like_num,"좋아요아이디"]="String"
            DonggukTime.df_timeline.loc[like_num,"좋아요아이디"]=temp
            DonggukTime.df_timeline.loc[like_num,"좋아요수"]=1
            DonggukTime.df_timeline.to_excel("timeline.xlsx",index=False)
            print("좋아요 누르기 완료!\n")
        else:
            if self.id in DonggukTime.df_timeline["좋아요아이디"].iloc[like_num].split():
                print("이미 좋아요를 누르셨습니다!\n")
            else:
                temp=temp+" "+self.id
                DonggukTime.df_timeline.loc[like_num,"좋아요아이디"]="String"
                DonggukTime.df_timeline.loc[like_num,"좋아요아이디"]=temp
                number=len(list(temp.split()))
                DonggukTime.df_timeline.loc[like_num,"좋아요수"]=number
                DonggukTime.df_timeline.to_excel("timeline.xlsx",index=False)
                print("좋아요 누르기 완료!\n")
    #회원탈퇴하기
    def secession(self):
        index_num_delete=0
        for i in range(len(DonggukTime.df_idpw)):
            if DonggukTime.df_idpw["아이디"][i]==self.id:
                index_num_delete=i
                break
        DonggukTime.df_idpw.drop(DonggukTime.df_idpw.index[index_num_delete],inplace=True)
        DonggukTime.df_idpw.to_excel("ID,PW.xlsx",index=False)
        print("회원탈퇴 성공!\n")
    def id_return(self):
        return self.id
    def crawling(self):
        sw_url="https://itcec.dongguk.edu/bbs/board.php?bo_table=itedu4_11&page=2&page=1"
        sw_res= requests.get(sw_url)
        #혹시나 프로그램에 문제가 생기면 종료를 하도록 함.
        sw_res.raise_for_status()
        #sw_soup은 모든 정보를 가지고 있다.
        sw_soup=BeautifulSoup(sw_res.text,"lxml")
        sw_info1=sw_soup.table.td.find_all("a",attrs={"style":"font-weight:bold;color:#000000;"})
        #공지사항(공지)
        ballground=[]
        for i in sw_info1:
            ballground.append(i.get_text())
        a_tag=sw_soup.select("a")
        result=[]
        for i in a_tag:
            result.append(i.get_text())
        del result[:result.index(ballground[0])]
        del result[:result.index(ballground[-1])]
        result=[i for i in result if len(i)>5]
        print()
        print("<< 공지글 >>")
        for i in ballground:
            print(i)
        print()
        print("<< 일반글 >>")
        for i in result:
            print(i)
        print()
        print("링크 : https://itcec.dongguk.edu/bbs/board.php?bo_table=itedu4_11&page=2&page=1")
        print()
    def rank(self):
        print()
        print("<< 과목 평점 RANKING >>")
        head_name=[i for i in DonggukTime.df_timeline["과목명"]]
        head_name=list(set(head_name))
        for_rank=[]
        a=DonggukTime.df_timeline[["과목명","평점"]]
        for i in head_name:
            for_rank.append([i,round(a["평점"].loc[a["과목명"]==i].mean(),4)])
        for_rank=sorted(for_rank, key=lambda x:x[1],reverse=True)
        for i,j in enumerate(for_rank):
            print("{} - {} :\t{}점".format(i+1,j[0],j[1]))
        print()


#로그인 함수
def main():
    print("회원 가입 하기 >> 1\n로그인 하기 >> 2\n가입된 회원 정보 >> 3")
    while 1 :
        a=int(input())
        if a==1:
            name=input("성함을 입력해 주세요. >>")
            while 1:
                try:
                    birth=input("주민번호 앞 6자리(생년월일)를 입력해 주세요. >>")
                    #6자리로 입력하지 않은 경우!
                    if len(str(birth))!=6:
                        print("띄어쓰기 없이 6자리로 입력해주세요!")
                    else:
                        break
                except :
                    #주민번호를 숫자가아니라 문자열로 입력한 경우
                    print("숫자를 입력해주세요!")
            #중복되는 아이디가 없게 한다.
            id_sign=False
            while 1:
                id=input("ID 를 입력해 주세요.  >>")
                #입력한 ID가 DataFrame안에 있는지 확인
                if sum(DonggukTime.df_idpw["아이디"].astype("str").str.contains(id))>0:
                    print("이미 존재하는 ID 입니다. ID를 다시 입력해주세요!")
                else:
                    break
            #패스워드를 두번 받고 그게 같으면 비밀 번호가 된다.
            while 1:
                pw=input("Password 를 입력해 주세요. >>")
                pw_2=input("Password 를 다시 입력해 주세요. >>")
                if pw !=pw_2:
                    print("패스워드가 다릅니다 다시 입력해 주세요.\n")
                else:
                    break

            print()
            #엑셀에 개인정보 저장
            DonggukTime.df_idpw=pd.read_excel("ID,PW.xlsx")
            DonggukTime.df_idpw=DonggukTime.df_idpw.append({"아이디":id,"패스워드":pw,"생년월일":birth,"이름":name},ignore_index=True)
            DonggukTime.df_idpw.to_excel("ID,PW.xlsx",index=False)
            print("회원가입 완료!")
            print()
            print("회원 가입 하기 >> 1\n로그인 하기 >> 2\n")
        elif a==2:
            #Boolean형태로 로그인이 되면 True로 바뀌게
            log_in_sign=False
            log_in_id=input("ID를 입력해 주세요 >>")
            log_in_pw=input("Password를 입력해 주세요 >>")
            print()
            for i in range(len(DonggukTime.df_idpw)):
                if (log_in_id ==DonggukTime.df_idpw["아이디"][i]) and (log_in_pw == str(DonggukTime.df_idpw["패스워드"][i])):
                    #로그인이 된 상태
                    log_in_sign=True
                    #로그인한 객체의 리스트 index를 클래스 변수에 저장한다.
                    DonggukTime.user_index=i
                    break
            if log_in_sign:
                print("로그인 완료\n")
                break
            else:
                #로그인 실패(객체에 저장된 아이디와 비번이 틀린경우)
                print("ID 혹은 Password를 다시 확인해 주세요")
                print()
                print("회원 가입 하기 >> 1\n로그인 하기 >> 2\n가입된 회원 정보 >> 3")
        elif a==3:
            for i in range(len(DonggukTime.df_idpw)):
                print("{}. \n이름 : {}\n생년월일 : {}\n아이디 : {}".format(i+1,DonggukTime.df_idpw["이름"][i],DonggukTime.df_idpw["생년월일"][i],DonggukTime.df_idpw["아이디"][i]))
                print()
            print("회원 가입 하기 >> 1\n로그인 하기 >> 2\n가입된 회원 정보 >> 3")

        else:
            #1,2번중 하나를 입력하지 않은 경우!
            print("1번 혹은 2번만 입력해 주세요!")


while 1:
    main() #로그인 하기
    user_index=DonggukTime.user_index
    user=DonggukTime([DonggukTime.df_idpw["이름"][user_index],DonggukTime.df_idpw["아이디"][user_index],DonggukTime.df_idpw["패스워드"][user_index],DonggukTime.df_idpw["생년월일"][user_index]])
    user.show_timeline()
    print()
    while 1:
        a=int(input("<< 작업 선택 >>\n\n1 - 타임라인 보기\n2 - 타임라인 작성\n3 - 타임라인 글 삭제\n4 - 비밀번호 변경\n5 - 댓글 달기\n6 - 좋아요 누르기\n8 - 회원 탈퇴\n9 - 선 이수과목 조회\n10 - 강의 평점 순위\n11 - 융합소프트웨어 공지사항\n0 - 로그아웃\n"))
        if a==1:
            #타임라인 보기
            user.show_timeline()
        elif a==2:
            #타밈라인 글 쓰기
            user.write_timeline()
        elif a==3:
            #글 삭제
            if sum(DonggukTime.df_timeline["아이디"].astype("str").str.contains(user.id_return()))>0:
                user.delete_post()
            else:
                #내가 작성한 글이 없을때
                print("본인은 작성한 글이 없습니다. ")
                print()
        elif a==4:
            #password변경
            user.edit_profile_pw()
        elif a==5:
            #댓글 쓰기
            user.write_comment()
        elif a==6:
            user.like()
        elif a==8:
            #실수로 눌렀을경우를 방지 하기위해 단계를 걸어줌
            b=int(input("정말로 회원 탈퇴를 하시겠습니까?\n1 - 예\n2- 아니요\n>>"))
            if b==1:
                #회원탈퇴
                user.secession()
                #회원탈퇴후 로그인 화면으로 가게끔
                break
            else:
                pass
        elif a==9:
            #선이수과목조회
            user.standing_mc_the_max()
        elif a==10:
            user.rank()
        elif a==11:
            user.crawling()
        elif a==0:
            #로그인 창으로 가게 만듬
            break
