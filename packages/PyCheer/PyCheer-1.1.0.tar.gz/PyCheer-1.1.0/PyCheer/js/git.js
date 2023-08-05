async function checkout(branch)
{
    var confirm_value;
    await swal({"text":"确定切换至"+branch+"分支吗？","buttons":["取消","确认"]}).then((value)=>{confirm_value=value;});
    if(confirm_value)
    {
        try
        {
            const response = await axios.post("/git/checkout?branch="+branch);
            console.log(response);
            if(response.status==200)
            {
                await swal({"text":"切换成功。","icon":"success"});
                location.reload();
            }
        }
        catch(err)
        {
            await swal({"text":"切换失败。您可以查看服务控制台输出内容。","icon":"error"});
        }
    }
}
async function new_remote_branch()
{
    var remote_branch_name;
    await swal({"text":"远程分支名：","content":"input","buttons":["取消","确认"]}).then((value)=>{remote_branch_name=value;});
    if(!remote_branch_name)
    {
        return;
    }
    var remote_url;
    await swal({"text":"远程URL：","content":"input","buttons":["取消","确认"]}).then((value)=>{remote_url=value;});
    if(!remote_url)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/new_remote?name="+remote_branch_name+"&url="+remote_url);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"新建成功。","icon":"success"});
            location.reload();
        }
    }
    catch(err)
    {
        await swal({"text":"新建失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function remove_remote(name)
{
    var confirm_value;
    await swal({"text":"确定删除远程分支"+name+"吗？","buttons":["取消","确认"]}).then((value)=>{confirm_value=value;});
    if(!confirm_value)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/remove_remote?name="+name);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"删除成功。","icon":"success"});
            location.reload();
        }
    }
    catch(err)
    {
        await swal({"text":"删除失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function new_branch()
{
    var name;
    await swal({"text":"分支名：","content":"input","buttons":["取消","确认"]}).then((value)=>{name=value;});
    if(!name)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/new_branch?name="+name);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"新建成功。","icon":"success"});
            location.reload();
        }
    }
    catch(err)
    {
        await swal({"text":"新建失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function get_status()
{
    try
    {
        const response = await axios.post("/git/status");
        console.log(response)
        if(response.status==200)
        {
            var content=decodeURIComponent(response.data.result)
            document.getElementById("status").innerHTML=content;
        }
    }
    catch(err)
    {
        await swal({"text":"获取文件编辑信息失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
get_status();
async function stage()
{
    try
    {
        const response = await axios.post("/git/stage");
        console.log(response)
        if(response.status==200)
        {
            get_status();
            await swal({"text":"暂存成功。","icon":"success"});
        }
    }
    catch(err)
    {
        await swal({"text":"暂存失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function commit()
{
    var info;
    await swal({"text":"请输入提交信息。不支持多行文本。","content":"input","buttons":["取消","确认"]}).then((value)=>{info=value;});
    if(!info)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/commit?info="+encodeURIComponent(info));
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"提交成功。","icon":"success"});
            get_status();
        }
    }
    catch(err)
    {
        await swal({"text":"提交失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function pull(remote,branch)
{
    var confirm_value;
    await swal({"text":`确认拉取远程分支${remote}到本地分支${branch}吗？`,"buttons":["取消","确认"]}).then((value)=>{confirm_value=value;});
    if(!confirm_value)
    {
        return;
    }
    try
    {
        const response = await axios.post(`/git/pull?remote=${remote}&branch=${branch}`);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"拉取成功。","icon":"success"});
            get_status();
        }
    }
    catch(err)
    {
        await swal({"text":"拉取失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}
async function push(remote,branch)
{
    var confirm_value;
    await swal({"text":`确认推送本地分支${branch}到远程分支${remote}吗？`,"buttons":["取消","确认"]}).then((value)=>{confirm_value=value;});
    if(!confirm_value)
    {
        return;
    }
    try
    {
        const response = await axios.post(`/git/push?remote=${remote}&branch=${branch}`);
        console.log(response)
        if(response.status==200)
        {
            await swal({"text":"推送成功。","icon":"success"});
            get_status();
        }
    }
    catch(err)
    {
        await swal({"text":"推送失败。您可以查看服务控制台输出内容。","icon":"error"});
    }
}