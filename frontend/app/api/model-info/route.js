import { NextResponse } from 'next/server';
import path from 'path';
import { execSync } from 'child_process';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    // Use Python to load the pickle and extract model info as JSON
    const scriptPath = path.join(process.cwd(), '..', 'backend', 'extract_model_info.py');
    const output = execSync(`python "${scriptPath}"`, {
      cwd: path.join(process.cwd(), '..', 'backend'),
      timeout: 15000,
    }).toString();

    const data = JSON.parse(output);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
