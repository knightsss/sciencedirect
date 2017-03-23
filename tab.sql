������
create database db_sciencedirect    


    ���߱�
    create table db_sciencedirect.t_sciencedirect_journals_author(
    author_id varchar(20),
    article_url varchar(100), 
    author_name varchar(100),
    author_affiliation varchar(500),
    author_emails varchar(100),
    author_correspondences varchar(200)
    )
    
    
    �ڿ����ݱ�
    create table db_sciencedirect.t_sciencedirect_journals_article(
    article_id varchar(20),
    article_url varchar(100),   #   �ڿ����ĵ�ΨһURL http://www.sciencedirect.com/science/article/pii/S2212671614001024
    publication_title varchar(100),    #   AASRI Procedia
    volume varchar(100),   #  Volume 9, 2014, Pages 2-7
    article_title varchar(200),   #   A New Texture Analysis Approach for Iris Recognition
    author_group varchar(200),     #���������Ϣ
    doilink varchar(100),    #����  http://dx.doi.org/10.1016/j.actbio.2017.01.035
    abstract_author text,    #ժҪ
    keywords varchar(200)  #�ؼ���
    )
    
    
    URL��ϵ��
    create table db_sciencedirect.t_sciencedirect_journals_url(
    url_id varchar(20),
    main_url varchar(100),   #   ��ҳ��ÿ��ѡ���URL    /science/journal/22126716
    volume_url varchar(100),   #  ��ҳÿ��ѡ�������µĶ�Ӧ�ľ�URL   http://www.sciencedirect.com/science/journal/22126716     #href: /science/journal/22126716/9
    article_url varchar(100)   #   ÿ���Ӧ���ڿ���URL��Ψһ��    http://www.sciencedirect.com/science/article/pii/S2212671614001024
    )

    #����
    create table db_sciencedirect.t_sciencedirect_journals_class(
    class_id varchar(20),
    subject_name varchar(200),   #   ���⡢��Ŀ
    son_subject_name varchar(200),    #  �� ���⡢��Ŀ
    grandson_subject_name varchar(200),   #  ���� ���⡢��Ŀ
    main_url varchar(200)   #   ��ҳ��ÿ��ѡ���URL    /science/journal/22126716
    )