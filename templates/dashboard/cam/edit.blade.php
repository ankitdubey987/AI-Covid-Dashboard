@extends('dashboard.admin')

@section('content')
<div class="container">
    <div class="col-md-6 offset-md-4 m-auto">
        <form class="form-group" action="{{ route('team.update',$team->id) }}" method="post"
            enctype="multipart/form-data">
            <input type="text" name="name" id="InputName" placeholder="Name" class="form-control my-2" value="{{$team->teammateName}}">
            <input type="file" name="photo" id="InputImage" class="form-control my-2" value="{{$team->thumbnail}}">
            <input type="text" name="jobrole" id="InputJobRole" class="form-control my-2" placeholder="Job Role" value="{{$team->jobrole}}">
            <input type="submit" value="Update Team" class="btn btn-primary offset-md-5">
            @csrf
            @method('PUT')

        </form>
    </div>
</div>
@endsection
