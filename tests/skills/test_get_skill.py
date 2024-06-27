from uuid import uuid1

from camel_converter import dict_to_camel
from playhouse.shortcuts import model_to_dict

from database.models.projects import Projects
from database.models.skills import Skills
from database.models.skills_projects import SkillsProjects


def test_get_skill_and_your_projects(client):
    random_id = uuid1()
    skill = Skills.create(title=f"Title {random_id}")
    projects = []
    for i in range(5):
        project = Projects.create(
            title=f"Title test {random_id} {i}",
            description=f"Description test {random_id} {i}",
            snapshot=f"http://snapshot.com/image-{random_id}-{i}.jpg",
            repository_link=f"http://repository.com/my-{random_id}-{i}.git",
            start="2024/03/22",
            last_update="2024/06/13",
        )
        projects = [*projects, dict_to_camel(model_to_dict(project))]
        SkillsProjects.create(project_id=project.id, skill_id=skill.id)
    response = client.get(
        f"api/skill/{skill.id}", content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json == {**model_to_dict(skill), "projects": projects}


def test_get_all_skills_without_projects(client):
    random_id = uuid1()
    Skills.delete()
    skills = [Skills(title=f"Test skill {random_id} - {i}") for i in range(5)]
    skills_list = [model_to_dict(skill) for skill in skills]
    Skills.bulk_create(skills)
    response = client.get("api/skills", content_type="application/json")
    without_id = list(map(lambda skill: del(skill["id"]), response.json))

    assert response.status_code == 200
    assert without_id == skills_list
